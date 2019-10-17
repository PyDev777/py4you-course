(function ($) {
 "use strict";
    
/*-----------------------------
	Menu Stick
---------------------------------*/
    $(window).on('scroll',function() {
        if ($(this).scrollTop() > 1){  
            $('.sticker').addClass("stick");
        }   
        else{
            $('.sticker').removeClass("stick");
        }
    });
    
/*----------------------------
    Toogle Search
------------------------------ */
    // Handle click on toggle search button
    $('.header-search').on('click', function() {
        $('.search').toggleClass('open');
        return false;
    });
    
/*----------------------------
    jQuery MeanMenu
------------------------------ */
	jQuery('nav#dropdown').meanmenu();	
	
    
/*----------------------------
    Nivo Slider Active
------------------------------ */
    $('#nivoslider').nivoSlider({
        effect: 'random',
        slices: 15,
        boxCols: 10,
        boxRows: 10,
        animSpeed: 500,
        pauseTime: 5000,
        startSlide: 0,
        directionNav: true,
        controlNavThumbs: false,
        pauseOnHover: false,
        manualAdvance: true
    });
/*----------------------------
    Wow js active
------------------------------ */
    new WOW().init();
 
/*--------------------------
    ScrollUp
---------------------------- */	
	$.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    }); 	   
    
/*--------------------------
    Counter Up
---------------------------- */	
    $('.counter').counterUp({
        delay: 70,
        time: 5000
    }); 

/*------------------------------------
	Textilate Activation
--------------------------------------*/
    $('.tlt').textillate({
        loop: true,
        minDisplayTime: 2500
    });
    
/*------------------------------------
	ColorSwitcher

    $('.ec-handle').on('click', function(){
        $('.ec-colorswitcher').trigger('click')
        $(this).toggleClass('btnclose');
        $('.ec-colorswitcher') .toggleClass('sidebarmain');
        return false;
    });
    $('.ec-boxed,.pattren-wrap a,.background-wrap a').on('click', function(){
        $('.as-mainwrapper').addClass('wrapper-boxed');
        $('.as-mainwrapper').removeClass('wrapper-wide');
    });
    $('.ec-wide').on('click', function(){
        $('.as-mainwrapper').addClass('wrapper-wide');
        $('.as-mainwrapper').removeClass('wrapper-boxed');
    });
--------------------------------------*/

/*------------------------------------
	Magnific Popup Active
--------------------------------------*/
    $('.popup-image').magnificPopup({
      type: 'image',
      gallery:{
                enabled:true
            }
      // other options
    });
    
    // $('#search_input').keypress(function (event) {
    //     if (event.keyCode === 10 || event.keyCode === 13) {
    //         event.preventDefault();
    //     }
    // });


})(jQuery); 