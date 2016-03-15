$(document).ready(function(){
    $(".button-collapse").sideNav();
    $('select').material_select();
    $('#id_note').val('New Text');
    $('#id_note').trigger('autoresize');
    $('textarea#id_note').characterCounter();
});
