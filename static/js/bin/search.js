$(document).ready(function(){
    var $invitation_rows = $('#invitation-rows tr');
    var $guest_rows = $('#guest-rows tr');
    var $attendee_rows = $('#attendee-rows tr');
    $('#attendee-search').keyup(function() {
        var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
            reg = RegExp(val, 'i'),
            text;
        $attendee_rows.show().filter(function() {
            text = $(this).text().replace(/\s+/g, ' ');
            return !reg.test(text);
        }).hide();
    });
    $('#invitation-search').keyup(function() {
        var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
            reg = RegExp(val, 'i'),
            text;
        $invitation_rows.show().filter(function() {
            text = $(this).text().replace(/\s+/g, ' ');
            return !reg.test(text);
        }).hide();
    });
    $('#guest-search').keyup(function() {
        var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
            reg = RegExp(val, 'i'),
            text;
        $guest_rows.show().filter(function() {
            text = $(this).text().replace(/\s+/g, ' ');
            return !reg.test(text);
        }).hide();
    });
});
