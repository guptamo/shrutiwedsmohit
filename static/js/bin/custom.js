$(document).ready(function(){
    $(".button-collapse").sideNav();
    $('select').material_select();
    $('#id_note').val();
    $('#id_note').trigger('autoresize');
    $('.slider').slider(
        {
            "full_width": true,
            "height": 600,
            "indicators": false,
            "interval": 4000,
        });
    $('textarea#id_note').characterCounter();
});
