/*!
 * navbar-shadow.js
 *
 * show and hide navbar shadow
 */


$(function() {
    var navbar = $('.navbar-fixed-top');
    $(window).scroll(function(){
        if($(window).scrollTop() <= 20){
            navbar.css('box-shadow', 'none');
        } else {
            navbar.css('box-shadow', '0px 0.0625em 0.3125em rgba(0, 0, 0, 0.15)'); 
        }
    });  
});
