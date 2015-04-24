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

function skip_new_friend_callback(data) {
    //alert('skip_new_friend_callback');

    var p_instagram_user_id = data.p_instagram_user_id;
    var result = data.result;
    var new_friend_id = "#new_friend_" + p_instagram_user_id;
    var interactions_remaining = data.interactions_remaining;

    $('#interactions_remaining_text').html(interactions_remaining);

    $('html, body').animate({
        scrollTop: $(new_friend_id).offset().top - 50
    }, 600);
    $(new_friend_id).hide();

}

function skip_new_friend(p_instagram_user_id) {
    //alert('skip_new_friend');

    var button_id = '#skip_button_' + p_instagram_user_id;
    $(button_id).attr('disabled','disabled');

    Dajaxice.instagramuser.skip_new_friend(skip_new_friend_callback, {'p_instagram_user_id': p_instagram_user_id});
}


function remove_new_friend_callback(data) {
    //alert('remove_new_friend_callback');

    var p_instagram_user_id = data.p_instagram_user_id;
    var result = data.result;
    var new_friend_id = "#new_friend_" + p_instagram_user_id;

    $('html, body').animate({
        scrollTop: $(new_friend_id).offset().top - 50
    }, 600);
    $(new_friend_id).hide();

}

function remove_new_friend(p_instagram_user_id) {
    //alert('remove_new_friend');

    var button_id = '#remove_button_' + p_instagram_user_id;
    $(button_id).attr('disabled','disabled');

    Dajaxice.instagramuser.remove_new_friend(remove_new_friend_callback, {'p_instagram_user_id': p_instagram_user_id});
}

function analyze_for_friends_callback (data) {
    var result = data.result;
    var p_instagram_user_id = data.p_instagram_user_id;

    $('#analyze_result_' + p_instagram_user_id).html(result);
}


function analyze_for_friends(p_instagram_user_id) {
     Dajaxice.instagramuser.analyze_for_friends(analyze_for_friends_callback, {'p_instagram_user_id': p_instagram_user_id});
}