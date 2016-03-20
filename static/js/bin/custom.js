$(document).ready(function(){
    $(".button-collapse").sideNav();
    $('select').material_select();
    $('#id_note').val();
    $('#id_note').trigger('autoresize');
    $('.slider').slider(
        {
            "height": 600,
            "indicators": false,
        });
    $('textarea#id_note').characterCounter();
});
