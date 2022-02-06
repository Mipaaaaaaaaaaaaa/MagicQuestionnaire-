from django.shortcuts import render, redirect
from .backend import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from MipaSurvey import settings
from urllib.parse import quote
from django.http.response import StreamingHttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def debug(request):
    print('开始debug')
    return render(request, 'debug.html')

def index(request):
    print('进入主页！')
    context = {
        'success': False,
        'data': {}
    }
    if request.user.is_authenticated:
        context['data']['username'] = request.user.username
        try:
            context['data']['NickName'] = get_userinfo(request.user.username)
        except:
            context['data']['NickName'] = request.user.username
    else:
        context['data']['username'] = ''
        context['data']['NickName'] = '未登录用户'
    return render(request, 'index.html', {'jsondata': json.dumps(context),'htmldata':context})


def login(request):
    if request.user.is_authenticated:
        print('登陆过了！',request.user.username,)
        return redirect('/surveylist/')
    else:
        print('还没登陆！')
        return render(request, 'login.html')


def loginresult(request):
    print('in loginresult')
    print(request.body)
    data = json.loads(request.body)
    context = {
        'success': False,
        'data': {}
    }
    if data.get('type') == 'login':
        context['data']['type'] = 'login'
        username = data.get('username')
        password = data.get('password')
        userobj = auth.authenticate(username=username, password=password)
        if userobj is not None:
            auth.login(request, userobj)
            context['success'] = True
            #path = data.get('next') or '/surveylist/'+username
            return JsonResponse(context)
        else:
            context['data']['error_message'] = '用户名或密码错误'
            return JsonResponse(context)

    elif data.get('type') == 'register':
        context['data']['type'] = 'register'
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        nickname = data.get('nickname')
        try:
            phonenumber = int(data.get('phonenumber'))
        except:
            phonenumber = None
        if create_user(username, password, email, nickname, phonenumber):
            context['data']['username'] = username
            context['success'] = True
            path = data.get('next') or '/surveylist/'+username
            print("创建成功！")
            return JsonResponse(context)
        else:
            print("创建失败！")
            context['data']['error_message'] = '用户名已存在'
            return JsonResponse(context)
    else:
        return redirect('/')

@login_required
def userlogout(request):
    context = {
        'success': False,
        'data': {}
    }
    auth.logout(request)
    context['data']['messagetitle'] = '登出成功！'
    return render(request, 'handle.html', {'jsondata':json.dumps(context),'htmldata':context})

@login_required
def surveylist(request):
    print(request)
    context = {
        'success': False,
        'data': {}
    }
    list_S = get_surveylist(request.user.username)
    context['success'] = True
    context['data']['surveylist'] = list_S
    context['data']['nickname'] = get_userinfo(request.user.username)
    context['data']['username'] = request.user.username
    return render(request, 'surveylist.html', {'jsondata':json.dumps(context),'htmldata':context})


def surveydetail(request, UUID_S):
    context = {
        'success': False,
        'data': {}
    }
    success, survey_name, survey_description, survey_type, survey_status, list_Q = get_surveydetail(
        UUID_S)
    if request.user.is_authenticated:
        context['data']['username'] = request.user.username
        try:
            context['data']['NickName'] = get_userinfo(request.user.username)
        except:
            context['data']['NickName'] = request.user.username
    else:
        context['data']['username'] = ''
        context['data']['NickName'] = '未登录用户'
    if success:
        if survey_type == False:
            if not request.user.is_authenticated:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        if checkfilled(request, UUID_S):
            res={}
            res['data']={}
            res['data']['message']='这份问卷你已经填过了！非常感谢！'
            res['data']['messagetitle']='想要创建自己的问卷？'
            return render(request, 'handle.html',{'jsondata': json.dumps(res),'htmldata' :res})
        else:
            if list_Q is not None:
                if survey_status is False:
                    print('该问卷未开放')
                    res={}
                    res['data']={}
                    res['data']['message']='该问卷暂未开放'
                    res['data']['messagetitle']='该问卷暂未开放，请稍后再试'
                    return render(request, 'handle.html',{'jsondata': json.dumps(res),'htmldata' :res})
                else:
                    context['success'] = True
                    context['data']['survey_name'] = survey_name
                    context['data']['survey_description'] = survey_description
                    context['data']['survey_type'] = survey_type
                    context['data']['survey_status'] = survey_status
                    context['data']['questionlist'] = list_Q
                    context['data']['uuid_s'] = UUID_S
                    return render(request, 'surveydetail.html', {'jsondata': json.dumps(context), 'htmldata': context})
            else:
                print('未能成功获取题目列表')
                context['data']['message'] = '未能成功获取题目列表'
                context['data']['messagetitle'] = '创建问卷的笨蛋忘记添加题目了！'
            return render(request, 'handle.html', {'jsondata': json.dumps(context)})
    else:
        print('查找问卷失败')
        context['data']['message'] = '问卷不存在！'
        context['data']['messagetitle'] = '请检查网址是否正确！'
        return render(request, 'handle.html', {'jsondata': json.dumps(context),'htmldata' :context})


def filledsurvey(request, UUID_S):
    context = {
        'success': False,
        'data': {}
    }
    if request.user.is_authenticated:
        context['data']['username'] = request.user.username
        try:
            context['data']['NickName'] = get_userinfo(request.user.username)
        except:
            context['data']['NickName'] = request.user.username
    else:
        context['data']['username'] = ''
        context['data']['NickName'] = '未登录用户'
    data = json.loads(request.body)
    if checkfilled(request, UUID_S):
        context['data']['message'] = '谢谢！你已经填过这份问卷，或问卷已经关闭！'
        context['data']['messagetitle']='想要创建自己的问卷？'
        return render(request, 'handle.html', {'jsondata': json.dumps(context),'htmldata':context})
    else:
        answerlist = data.get('answer')
        username = request.user.username
        fill_survey(UUID_S, answerlist, username)
        context['success'] = True
        context['data']['message'] = '问卷已提交！谢谢！'
        res = render(request, 'handle.html', {'jsondata': json.dumps(context),'htmldata':context})
        res.set_cookie(key=UUID_S, value=1,max_age=604800)
        return res



@login_required
def downloadreport(request, UUID_S):
    context = {
        'success': False,
        'data': {}
    }
    if not checkeditpermission(request.user.username, UUID_S):
        context['data']['message'] = '你居然想下载别人问卷的报告？惩罚你退出！'
        auth.logout(request)
        return render(request, 'handle.html', {'jsondata': json.dumps(context),'htmldata':context})
    file_path,file_name = get_surveyreport(UUID_S)
    response = StreamingHttpResponse(iter_file(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; {}'.format(
        "filename*=utf-8''{}".format(quote(file_name))
    )
    return response

@login_required
def analysis(request, UUID_S):
    print('开始分析！')
    context = {
        'success': False,
        'data': {}
    }
    if request.user.is_authenticated:
        context['data']['username'] = request.user.username
        context['data']['NickName'] = get_userinfo(request.user.username)
    else:
        context['data']['username'] = ''
        context['data']['NickName'] = '未登录用户'
    if not checkeditpermission(request.user.username, UUID_S):
        context['data']['message'] = '你居然想康别人问卷的报告？惩罚你退出！'
        auth.logout(request)
        return render(request, 'handle.html', {'jsondata': json.dumps(context),'htmldata':context})
    SInfo , AList , QList = get_surveyanswer(UUID_S)
    context['data']['answerlist'] = AList
    context['data']['surveyinfo'] = SInfo
    context['data']['questionlist'] = QList
    return render(request, 'analysis.html', {'jsondata': json.dumps(context),'htmldata':context})

@login_required
def createsurvey(request):
    data = json.loads(request.body)
    context = {
        'success': True,
        'data': {},
    }
    surveyname = data.get('survey_name')
    survey_description = data.get('survey_description')
    survey_type = data.get('survey_type')
    uuid = editsurveyinfo(None,'create',request.user.username,surveyname,survey_description,survey_type)
    context['data']['UUID_S'] = uuid
    return JsonResponse(context)

@login_required
def deletesurvey(request,UUID_S):
    context = {
        'success':False,
        'data': {},
    }
    if checkeditpermission(request.user.username,UUID_S):
        editsurveyinfo(uuid_s=UUID_S,edit_type = 'delete')
        context['success'] = True
        return JsonResponse(context)
    else:
        context['data']['error_message'] = '无权修改'
        return JsonResponse(context)

@login_required
def surveyswitch(request,UUID_S):
    data = json.loads(request.body)
    context = {
        'success':False,
        'data': {},
    }
    if checkeditpermission(request.user.username,UUID_S):
        s_status = data.get('survey_status')
        editsurveyinfo(uuid_s= UUID_S,edit_type='status',survey_status=s_status)
        context['success'] = True
        return JsonResponse(context)
    else:
        context['data']['error_message'] = '无权修改'
        return JsonResponse(context)
    

@login_required
def editsurvey(request, UUID_S):
    context = {
        'success': True,
        'data': {},
    }
    if not checkeditpermission(request.user.username, UUID_S):
        context['data']['message'] = '你居然想编辑别人的问卷？惩罚你退出！'
        auth.logout(request)
        return render(request, 'handle.html', {'jsondata': json.dumps(context),'htmldata':context})
    success, survey_name, survey_description, survey_type, survey_status, list_Q = get_surveydetail(
        UUID_S)
    context['success'] = success
    context['data']['uuid_s']=UUID_S
    context['data']['questionlist'] = list_Q
    context['data']['survey_name'] = survey_name
    context['data']['survey_description'] = survey_description
    context['data']['survey_type'] = survey_type
    context['data']['survey_status'] = survey_status
    context['data']['nickname'] = get_userinfo(request.user.username)
    return render(request, 'editsurvey.html', {'jsondata': json.dumps(context),'htmldata':context})


@login_required
def editfinish(request, UUID_S):
    data = json.loads(request.body)
    context = {
        'success': False,
        'data': {}
    }
    if not checkeditpermission(request.user.username, UUID_S):
        context['data']['message'] = '你居然想编辑别人的问卷？惩罚你退出！'
        auth.logout(request)
        return render(request, 'handle.html', {'jsondata': json.dumps(context),'htmldata':context})
    survey_name = data.get('survey_name')
    survey_description = data.get('survey_description')
    survey_type = data.get('survey_type')
    survey_status = data.get('survey_status')
    list_Q = data.get('questionlist')
    bDelete = data.get('bDelete')
    belong2user = request.user.username
    edit_survey(UUID_S, belong2user, survey_name, survey_description,
                    survey_type, survey_status, list_Q, bDelete)
    return JsonResponse(context)


@login_required
def userdetail(request):
    context = {
        'success': True,
        'data': {}
    }
    print(get_userdetail(request.user.username))
    context['data']['username'], context['data']['NickName'], context['data']['phonenumber'],context['data']['email'] = get_userdetail(
        request.user.username)
    #return JsonResponse(context)
    return render(request, 'myhome.html', {'jsondata': json.dumps(context),'htmldata':context})

@login_required
def changeuserinfo(request):
    data = json.loads(request.body)
    context = {
        'success': False,
        'data': {}
    }
    print(data)
    edituser(request.user.username, password=data.get('password'), email=data.get('email'), nickname=data.get('nickname'), phone=data.get('phone'))
    return JsonResponse(context)
