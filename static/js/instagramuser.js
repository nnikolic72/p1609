/**
 * Created by tanja on 3/27/2015.
 */

function ajaxStop() {
    $('#spinner').hide();
}

function ajaxStart() {
    $('#spinner').show();
}
/*
 $( document ).ready( function() {
 $( '#searchSubmit' ).click( function() {
 q = $( '#q' ).val();
 $( '#results' ).html( '&nbsp;' ).load( '{% url demo_user_search %}?q=' + q );
 });
 });
 */

function analyze_user_callback(data) {
    //alert('analyze_user_callback');

    var already_exists = data.already_exists;
    var error = data.error;
    var error_message = data.error_message;
    var html_text = data.html_text;
    var analyze_button = '#analyze_button';

    var id_bestphotos_div = '#bestphotos';
    $('#analyze_text').html('Analyze');

    $(id_bestphotos_div).html(html_text);

    ajaxStop();
}

function analyze_user() {
    //alert('analyze_user');
    ajaxStart();
    var id_name = '#username';
    var analyze_button = '#analyze_button';
    //alert(id_name);
    var data = $(id_name).serializeObject();

    $('#analyze_text').html('Analyzing...');

    //alert(data);
    Dajaxice.instagramuser.analyze_user(analyze_user_callback, {'form': data});

}