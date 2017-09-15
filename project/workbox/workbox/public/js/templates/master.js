/*!
 * master.js
 *
 * js code for master.xhtml
 */


$(function() {
    // navbar shadow
    $(window).scroll(function(){
        if($(window).scrollTop() <= 20){
            $('.navbar-fixed-top').css('box-shadow', 'none');
        } else {
            $('.navbar-fixed-top').css('box-shadow', '0px 0.0625em 0.3125em rgba(0, 0, 0, 0.15)'); 
        }
    });
    // mouseover effects on elements
    $('#dev').on('mouseover mouseout', function () {
        var randomColor = '#' + Math.random().toString(16).slice(-6);
        $('.icon-heart').css('color', randomColor);
    });
    $('#brand-img').on('mouseover', function () {
        $(this).stop().fadeOut(0).attr('src', '/images/box.png').fadeIn(300);
    });
    $('#brand-img').on('mouseout', function () {
        $(this).stop().fadeOut(0).attr('src', '/images/favicon.ico').fadeIn(300);
    });
});
