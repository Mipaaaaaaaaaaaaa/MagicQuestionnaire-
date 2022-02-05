from django.http import HttpResponse
from .models import UserInfo, SurveyList, QuestionDetail, AnswerRecord
import uuid
import os
import xlwt
from django.conf import settings
# from django.contrib.auth.models import User

def create_user(uname, pw, mail, nname, phone):
    success = False
    try:
        s = UserInfo.objects.get(username=uname)
    except UserInfo.DoesNotExist:
        success = True
        UserInfo.objects.create_user(username=uname, password=pw,
                                 email=mail, NickName=nname, phonenumber=phone)
    return success

def get_userinfo(username):
    info = UserInfo.objects.filter(username=username)
    # print('nickname:',info[0])
    return info[0].NickName

def edituser(username, password=None, email=None, nickname=None, phone=None):
    user = UserInfo.objects.get(username=username)
    print(password,email,nickname,phone)
    if password != '':
        user.set_password(password)
    if email is not None:
        user.email = email
        user.save()
    if nickname is not None:
        user.NickName = nickname
        user.save()
    if phone is not None:
        user.phonenumber = phone
        user.save()


def get_userdetail(username):
    info = UserInfo.objects.get(username=username)
    return info.username,info.NickName,info.phonenumber,info.email

def getfillednumber(uuid_s):
    try:
        anslist = AnswerRecord.objects.filter(UUID_S=uuid_s,ANum=0)
        # print('有人写过', anslist,anslist.count())
    except:
        print('查找写过失败了')
        return 0
    else:
        return anslist.count()

def get_surveylist(uname):
    res = []
    s_list = SurveyList.objects.filter(username=uname)
    for s in s_list:
        s_tmp = {}
        s_tmp['UUID_S'] = s.UUID_S
        s_tmp['SurveyName'] = s.SurveyName
        s_tmp['SurveyDescription'] = s.SurveyDescription
        s_tmp['SurveyType'] = s.SurveyType
        s_tmp['SurveyStatus'] =s.SurveyStatus
        s_tmp['LastEditTime'] = s.LastEditTime.strftime("%Y-%m-%d %H:%M:%S")
        s_tmp['number'] = getfillednumber(s.UUID_S)

        res.append(s_tmp)
    # print('res:',res)
    return res

def get_surveyreport(survey_id):
    s_info = SurveyList.objects.get(UUID_S = survey_id)
    s_answer = AnswerRecord.objects.filter(
        UUID_S=survey_id).order_by('username')
    xls = xlwt.Workbook(encoding='utf-8', style_compression=2)
    sheet = xls.add_sheet(s_info.SurveyName, cell_overwrite_ok=True)
    sheet.write(0, 0, '回答者姓名')
    sheet.write(0, 1, '题号')
    sheet.write(0, 2, '选项/回答')
    sheet.write(0, 3, '时间')
    for i in range(len(s_answer)):
        sheet.write(i + 1, 0, s_answer.username)
        sheet.write(i + 1, 0, s_answer.ANum)
        sheet.write(i + 1, 0, s_answer.AOptions)
        sheet.write(i + 1, 0, s_answer.Time)
    file_path = './Reports/' + survey_id + '.xls'
    xls.save(file_path)
    file_path = os.path.join(settings.BASE_DIR, file_path)
    file_name = s_info.SurveyName+'.xls'
    # print('文件保存在：',file_path)
    return file_path, file_name


def get_surveyanswer(survey_id):
    s = SurveyList.objects.get(UUID_S=survey_id)
    a = AnswerRecord.objects.filter(
        UUID_S=survey_id).order_by('username')
    Q_list = QuestionDetail.objects.filter(UUID_S=survey_id)
    s_tmp = {}
    s_tmp['UUID_S'] = s.UUID_S
    s_tmp['SurveyName'] = s.SurveyName
    s_tmp['SurveyDescription'] = s.SurveyDescription
    s_tmp['SurveyType'] = s.SurveyType
    s_tmp['SurveyStatus'] =s.SurveyStatus
    s_tmp['LastEditTime'] = s.LastEditTime.strftime("%Y-%m-%d %H:%M:%S")
    s_tmp['number'] = getfillednumber(s.UUID_S)
    res_a = []
    for ans in a:
        a_tmp={}
        a_tmp['ANum'] = ans.ANum
        a_tmp['username'] = ans.username
        a_tmp['AOption']=ans.AOptions
        a_tmp['Time']=ans.Time.strftime("%Y-%m-%d %H:%M:%S")
        res_a.append(a_tmp)
    res_QList = []
    for Q in Q_list:
        res_Q = {}
        res_Q['QNumber'] = Q.QNumber
        res_Q['QType'] = Q.QType
        res_Q['QDescription'] = Q.QDescription
        res_Q['QOptions'] = Q.QOptions
        res_Q['QTitle'] = Q.QTitle
        res_QList.append(res_Q)
    return s_tmp, res_a, res_QList


def get_surveydetail(survey_id):
    try:
        s_detail = SurveyList.objects.get(UUID_S=survey_id)
        print('找到问卷：',survey_id)
    except SurveyList.DoesNotExist:
        return False, 'unknown', None, None, None, None
    Q_list = QuestionDetail.objects.filter(UUID_S=survey_id)
    res_Qlist = []
    for Q in Q_list:
        res_Q = {}
        res_Q['QNumber'] = Q.QNumber
        res_Q['QType'] = Q.QType
        res_Q['QDescription'] = Q.QDescription
        res_Q['QOptions'] = Q.QOptions
        res_Q['QTitle'] = Q.QTitle
        res_Qlist.append(res_Q)
    survey_name = s_detail.SurveyName
    survey_description = s_detail.SurveyDescription
    survey_type = s_detail.SurveyType
    survey_status = s_detail.SurveyStatus
    print(True, survey_name, survey_description, survey_type, survey_status, res_Qlist)
    return True, survey_name, survey_description, survey_type, survey_status, res_Qlist


def checkeditpermission(uname, P_UUID_S):
    try:
        s = SurveyList.objects.get(username=uname, UUID_S=P_UUID_S)
        success = True
    except SurveyList.DoesNotExist:
        success = False
    return success

def editsurveyinfo(uuid_s=None,edit_type=None,belong2user=None,s_name=None,s_description=None,s_type=None,survey_status = True):
    if edit_type == 'create':
        uuid_s = genUUID()
        s = SurveyList(UUID_S=uuid_s, username=belong2user, SurveyName=s_name,
                   SurveyDescription=s_description, SurveyType=s_type)
        s.save()
        return uuid_s
    elif edit_type == 'status':
        try:
            s = SurveyList.objects.filter(UUID_S=uuid_s)
            s.SurveyStatus = survey_status
            s.save()
            success = True
        except:
            success = False
        return success
    elif edit_type == 'delete':
        try:
            SurveyList.objects.filter(UUID_S=uuid_s).delete()
            QuestionDetail.objects.filter(UUID_S=uuid_s).delete()
            AnswerRecord.objects.filter(UUID_S=uuid_s).delete()
            success = True
        except:
            success = False
        return success
    else:
        return False


def fill_survey(uuid_s, answerlist, username):
    for ans in answerlist:
        a = AnswerRecord(UUID_S=uuid_s, username=username, ANum=ans['ANum'], AOptions=ans['AOptions'])
        a.save()

def edit_survey(uuid_s, belong2user, s_name, s_description, s_type, survey_status,editlist):
    try:
        SurveyList.objects.get(UUID_S=uuid_s)
    except:
        uuid_s = genUUID()
    else:
        SurveyList.objects.filter(UUID_S=uuid_s).delete()
        print('删除：',uuid_s)
    s = SurveyList(UUID_S=uuid_s, username=belong2user, SurveyName=s_name,
                   SurveyDescription=s_description, SurveyStatus=survey_status, SurveyType=s_type)
    s.save()
    QuestionDetail.objects.filter(UUID_S=uuid_s).delete()
    for qedit in editlist:
        print('qlist:',qedit)
        print('qdesc',qedit['QDescription'])
        q = QuestionDetail(UUID_S=uuid_s, QNumber=qedit['QNumber'],
                           QType=qedit['QType'], QDescription=qedit['QDescription'], QOptions=qedit['QOptions'], QTitle=qedit['QTitle'])
        q.save()
    AnswerRecord.objects.filter(UUID_S=uuid_s).delete()

def iter_file(path, size=1024):
    with open(path, "rb", ) as f:
        for data in iter(lambda: f.read(size), b''):
            yield data

def genUUID():
    uuidexist = True
    while uuidexist:
        gen_uuid = uuid.uuid4()
        try:
            s = SurveyList.objects.get(UUID_S=gen_uuid)
            uuidexist = True
        except SurveyList.DoesNotExist:
            uuidexist = False
    return gen_uuid


def checkfilled(request, P_UUID_S):
    filled = False
    sdetail = SurveyList.objects.get(UUID_S=P_UUID_S)
    if sdetail.SurveyType == True:
        try:
            hascookie = request.COOKIE.get(P_UUID_S)
            print('cookie exists',hascookie.values())
        except:
            filled = True
    else:
        try:
            hasname = AnswerRecord.objects.get(username=request.user.username)
        except:
            filled = True
    print('填过',filled)
    return filled

