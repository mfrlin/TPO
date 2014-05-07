$(document).ready(function () {
    var c = $(".btn.btn-small.h");

    c.click(function(){
        var btn = $(this).children("span");
        var cl = btn[0].className;
        if (cl === 'icon-plus'){
            console.log('plus');
            btn.removeClass(cl).addClass('icon-minus');
        }
        else{
            console.log('minus');
            btn.removeClass(cl).addClass('icon-plus');
        }
    });
});