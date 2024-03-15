// doesn't rely on css for switching; forked from http://jsfiddle.net/FvMYz/
$(function() {
    $('.content').hide();
    $('#selectField').change(function() {
       $('.content').hide();
       $('#' + $(this).val()).show();
    });
 });