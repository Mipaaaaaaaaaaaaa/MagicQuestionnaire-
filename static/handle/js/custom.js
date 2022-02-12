/*	################################################################
	File Name: custom.js
	Template Name: Pori
	Created By: RevolTheme
	http://revoltheme.com

	1) PRELOADER
	2) STICKY MENU
	3) ANCHOR TAG CLICK ANIMATION
    4) COLLAPSE SCRIPT
    5) ISOTOPE WORK
    6) OWL CLIENT ACTIVATION
    7) OWL TESTIMONIAL ACTIVATION
    8) SKILL PROGRESS BAR
    9) COUNTER UP
    10) LINK SCROLL ANIMATION
    11) PRETTY PHOTO
    12) CONTACT FORM
    13) SCROLL ANIMATION

################################################################# */

$('document').ready(function() {

    "use strict";

    /*==============================
        PRELOADER
    ===============================*/
    (function($){
        $(window).load(function() {
    	    $('#preloader').hide();
        });
    })(jQuery);

    /*==============================
       STICKY MENU
    ==============================*/
    (function($){
        // menu fixed
        var navHeight = 50;
        var nav = $('.header-section');
        $(window).scroll(function () {
            if ($(this).scrollTop() > navHeight ) {
                nav.addClass("fixed");
            } else {
                nav.removeClass("fixed");
            }
        });

        var lastId,
        topMenu = $(".navbar-nav"),
        topMenuHeight = topMenu.outerHeight()+15,
        menuItems = topMenu.find("a"),
        scrollItems = menuItems.map(function(){
            var item = $($(this).attr("href"));
            if (item.length) { return item; }
        });

        // so we can get a fancy scroll animation
        menuItems.click(function(e){
            var href = $(this).attr("href"),
                offsetTop = href === "#" ? 0 : $(href).offset().top-topMenuHeight+1;
            $('html, body').stop().animate({
                scrollTop: offsetTop
            }, 300);
            e.preventDefault();
        });

        // Bind to scroll
        $(window).scroll(function(){
            var fromTop = $(this).scrollTop()+topMenuHeight;
            var cur = scrollItems.map(function(){
                if ($(this).offset().top < fromTop)
                return this;
            });
           cur = cur[cur.length-1];
           var id = cur && cur.length ? cur[0].id : "";
           if (lastId !== id) {
                lastId = id;
                menuItems
                 .parent().removeClass("active")
                 .end().filter("[href=#"+id+"]").parent().addClass("active");
            }
        });
    })(jQuery);

    /*==============================
        ANCHOR TAG CLICK ANIMATION
    ==============================*/
    (function($){
        $('.go-to-about').click(function(){
            $('html, body').animate({
                scrollTop: $( $(this).attr('href') ).offset().top
            }, 500);
            return false;
        });
    })(jQuery);


    /*==============================
        COLLAPSE SCRIPT
    ==============================*/
    (function($){
        $( ".panel .collapse.in" ).prev().addClass("title-active");
    })(jQuery);


    /*==============================
        ISOTOPW WORK
    ==============================*/
    (function($){
        $(window).load(function() {
            // init Isotope
            var $grid = $('.portfolio').isotope({
              itemSelector: '.portfolio-items',
              layoutMode: 'fitRows'
            });
            // filter functions
            var filterFns = {
              // show if number is greater than 50
            numberGreaterThan50: function() {
                var number = $(this).find('.number').text();
                return parseInt( number, 10 ) > 50;
            },
              // show if name ends with -ium
            ium: function() {
                var name = $(this).find('.name').text();
                return name.match( /ium$/ );
              }
            };
            // bind filter button click
            $('.filters-list').on( 'click', 'li', function() {
              var filterValue = $( this ).attr('data-filter');
              // use filterFn if matches value
              filterValue = filterFns[ filterValue ] || filterValue;
              $grid.isotope({ filter: filterValue });
            });
            // change is-checked class on buttons
            $('.button-group').each( function( i, buttonGroup ) {
              var $buttonGroup = $( buttonGroup );
              $buttonGroup.on( 'click', 'li', function() {
                $buttonGroup.find('.active').removeClass('active');
                $( this ).addClass('active');
              });
            });
        });

    })(jQuery);

    /*==============================
        OWL QUOTE ACTIVATION
    ==============================*/
    (function($){
        var owl = $("#testimonial");
        owl.owlCarousel({
            items : 1,
            itemsDesktop : [1000,1],
            itemsDesktopSmall : [900,1],
            itemsTablet: [600,1],
            itemsMobile : false
        });

        // Custom Navigation Events
        $(".testimonial-next").click(function(){
            owl.trigger('owl.next');
        })
        $(".testimonial-prev").click(function(){
            owl.trigger('owl.prev');
        })
    })(jQuery);


    /*==============================
        OWL CLIENT ACTIVATION
    ==============================*/
    (function($){
        var owl = $("#recent-work");
        owl.owlCarousel({
            items : 1,
            itemsDesktop : [1000,1],
            itemsDesktopSmall : [900,1],
            itemsTablet: [600,1],
            itemsMobile : false
        });
        $(".recent-next").click(function(){
            owl.trigger('owl.next');
        })
        $(".recent-prev").click(function(){
            owl.trigger('owl.prev');
        })
    })(jQuery);

    /*==============================
        OWL TESTIMONIAL ACTIVATION
    ==============================*/
    (function($){
        var owl = $("#client");
        owl.owlCarousel({
            items : 4,
            itemsDesktop : [1100,3],
            itemsDesktop : [1000,2],
            itemsDesktopSmall : [900,1],
            itemsTablet: [600,1],
            itemsMobile : false
        });
        $(".client-next").click(function(){
            owl.trigger('owl.next');
        })
        $(".client-prev").click(function(){
            owl.trigger('owl.prev');
        })
    })(jQuery);

    /*==============================
        SKILL PROGRESS BAR
    ==============================*/
    (function($){
        jQuery('.skillbar').each(function() {
			jQuery(this).appear(function() {
				jQuery(this).find('.count-bar').animate({
					width:jQuery(this).attr('data-percent')
				},3000);
				var percent = jQuery(this).attr('data-percent');
				jQuery(this).find('.count').html('<span>' + percent + '</span>');
			});
		});
    })(jQuery);

    /*==============================
        COUNTER UP
    ==============================*/
    (function($){
        $('.counter').counterUp({
            delay: 10,
            time: 1000
        });
    })(jQuery);

     /*==============================
        LINK SCROLL ANIMATION
    ==============================*/
    (function($){
        $('.top-button').click(function(){
            $('html, body').animate({
                scrollTop: $( $(this).attr('href') ).offset().top
            }, 500);
            return false;
        });
         // menu fixed
        var navHeight = 50;
        var nav = $('.top-button');
        $(window).scroll(function () {
            if ($(this).scrollTop() > navHeight ) {
                nav.addClass("fixed");
            } else {
                nav.removeClass("fixed");
            }
        });

    (function () {
        var previousScroll = 50;

        $(window).scroll(function(){
           var currentScroll = $(this).scrollTop();
           if (currentScroll < previousScroll){
               $(".top-button").removeClass("b");
               $(".top-button").addClass("t");

           } else {
                $(".top-button").removeClass("t");
              $(".top-button").addClass("b");

           }
           previousScroll = currentScroll;
        });
    }());

     /*==============================
        PRETTY PHOTO
    ==============================*/
    (function($){
        $("area[data-gal^='prettyPhoto']").prettyPhoto();
        $(".gallery:first a[data-gal^='prettyPhoto']").prettyPhoto({animation_speed:'normal',theme:'pp_default',slideshow:3000, autoplay_slideshow: false, social_tools:''});
        $(".gallery:gt(0) a[data-gal^='prettyPhoto']").prettyPhoto({animation_speed:'fast',slideshow:10000, hideflash: true});
    })(jQuery);

})(jQuery);



    /*==============================
        CONTACT FORM
    ==============================*/

     jQuery('#contact-form').submit(function(){
		var action = jQuery(this).attr('action');

		jQuery("#message").slideUp(750,function() {
		jQuery('#message').hide();

 		jQuery('#submit')
			.after('<img src="images/ajax-loader.gif" class="loader" />')
			.attr('disabled','disabled');

		jQuery.post(action, {
			name: jQuery('#name').val(),
			email: jQuery('#email').val(),
			website: jQuery('#website').val(),
			subject: jQuery('#subject').val(),
			comments: jQuery('#comments').val()
		},
			function(data){
				document.getElementById('message').innerHTML = data;
				jQuery('#message').slideDown('slow');
				jQuery('#contact-form img.loader').fadeOut('slow',function(){jQuery(this).remove()});
				jQuery('#submit').removeAttr('disabled');
				if(data.match('success') != null) $('#contact-form').show('slow');
			}
		);

		});
		return false;
	});

});

/*==============================
    SCROLL ANIMATION
==============================*/
(function($){
     (function() {
      var Util,
        __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

      Util = (function() {
        function Util() {}

        Util.prototype.extend = function(custom, defaults) {
          var key, value;
          for (key in custom) {
            value = custom[key];
            if (value != null) {
              defaults[key] = value;
            }
          }
          return defaults;
        };

        Util.prototype.isMobile = function(agent) {
          return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(agent);
        };

        return Util;

      })();

      this.WOW = (function() {
        WOW.prototype.defaults = {
          boxClass: 'wow',
          animateClass: 'animated',
          offset: 0,
          mobile: true
        };

        function WOW(options) {
          if (options == null) {
            options = {};
          }
          this.scrollCallback = __bind(this.scrollCallback, this);
          this.scrollHandler = __bind(this.scrollHandler, this);
          this.start = __bind(this.start, this);
          this.scrolled = true;
          this.config = this.util().extend(options, this.defaults);
        }

        WOW.prototype.init = function() {
          var _ref;
          this.element = window.document.documentElement;
          if ((_ref = document.readyState) === "interactive" || _ref === "complete") {
            return this.start();
          } else {
            return document.addEventListener('DOMContentLoaded', this.start);
          }
        };

        WOW.prototype.start = function() {
          var box, _i, _len, _ref;
          this.boxes = this.element.getElementsByClassName(this.config.boxClass);
          if (this.boxes.length) {
            if (this.disabled()) {
              return this.resetStyle();
            } else {
              _ref = this.boxes;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                box = _ref[_i];
                this.applyStyle(box, true);
              }
              window.addEventListener('scroll', this.scrollHandler, false);
              window.addEventListener('resize', this.scrollHandler, false);
              return this.interval = setInterval(this.scrollCallback, 50);
            }
          }
        };

        WOW.prototype.stop = function() {
          window.removeEventListener('scroll', this.scrollHandler, false);
          window.removeEventListener('resize', this.scrollHandler, false);
          if (this.interval != null) {
            return clearInterval(this.interval);
          }
        };

        WOW.prototype.show = function(box) {
          this.applyStyle(box);
          return box.className = "" + box.className + " " + this.config.animateClass;
        };

        WOW.prototype.applyStyle = function(box, hidden) {
          var delay, duration, iteration;
          duration = box.getAttribute('data-wow-duration');
          delay = box.getAttribute('data-wow-delay');
          iteration = box.getAttribute('data-wow-iteration');
          return box.setAttribute('style', this.customStyle(hidden, duration, delay, iteration));
        };

        WOW.prototype.resetStyle = function() {
          var box, _i, _len, _ref, _results;
          _ref = this.boxes;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            box = _ref[_i];
            _results.push(box.setAttribute('style', 'visibility: visible;'));
          }
          return _results;
        };

        WOW.prototype.customStyle = function(hidden, duration, delay, iteration) {
          var style;
          style = hidden ? "visibility: hidden; -webkit-animation-name: none; -moz-animation-name: none; animation-name: none;" : "visibility: visible;";
          if (duration) {
            style += "-webkit-animation-duration: " + duration + "; -moz-animation-duration: " + duration + "; animation-duration: " + duration + ";";
          }
          if (delay) {
            style += "-webkit-animation-delay: " + delay + "; -moz-animation-delay: " + delay + "; animation-delay: " + delay + ";";
          }
          if (iteration) {
            style += "-webkit-animation-iteration-count: " + iteration + "; -moz-animation-iteration-count: " + iteration + "; animation-iteration-count: " + iteration + ";";
          }
          return style;
        };

        WOW.prototype.scrollHandler = function() {
          return this.scrolled = true;
        };

        WOW.prototype.scrollCallback = function() {
          var box;
          if (this.scrolled) {
            this.scrolled = false;
            this.boxes = (function() {
              var _i, _len, _ref, _results;
              _ref = this.boxes;
              _results = [];
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                box = _ref[_i];
                if (!(box)) {
                  continue;
                }
                if (this.isVisible(box)) {
                  this.show(box);
                  continue;
                }
                _results.push(box);
              }
              return _results;
            }).call(this);
            if (!this.boxes.length) {
              return this.stop();
            }
          }
        };

        WOW.prototype.offsetTop = function(element) {
          var top;
          top = element.offsetTop;
          while (element = element.offsetParent) {
            top += element.offsetTop;
          }
          return top;
        };

        WOW.prototype.isVisible = function(box) {
          var bottom, offset, top, viewBottom, viewTop;
          offset = box.getAttribute('data-wow-offset') || this.config.offset;
          viewTop = window.pageYOffset;
          viewBottom = viewTop + this.element.clientHeight - offset;
          top = this.offsetTop(box);
          bottom = top + box.clientHeight;
          return top <= viewBottom && bottom >= viewTop;
        };

        WOW.prototype.util = function() {
          return this._util || (this._util = new Util());
        };

        WOW.prototype.disabled = function() {
          return !this.config.mobile && this.util().isMobile(navigator.userAgent);
        };

        return WOW;

      })();

    }).call(this);


    wow = new WOW(
      {
        animateClass: 'animated',
        offset: 100
      }
    );
    wow.init();
})(jQuery);

