/**
 * Created by n.nikolic on 3/25/2015.
 */

function back_button() {

    parent.history.back();
    return false;

}

function forward_button() {

    parent.history.forward();
    return false;

}

//  Stops ENTER key in forms
function stopRKey(evt) {
    var evt = (evt) ? evt : ((event) ? event : null);
    var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
    if ((evt.keyCode == 13) && (node.type=="text"))  {return false;}
}

document.onkeypress = stopRKey;

function inline_comment_toggler(divId, p_photo_id, p_instagram_user_name, comment_number ) {
    //alert(divId + ' ' + p_photo_id + ' ' + p_instagram_user_name);
    $('#new_comment_' + p_photo_id + '_' + comment_number).val('@'+p_instagram_user_name+' ');
    $("#" + divId).toggle();
    $('#new_comment_' + p_photo_id + '_' + comment_number).focus();

}

//function display_ajax_img(p_div_id, p_static_url) {
//    var div_id = '#' + p_div_id;
//    var ajax_img = '<img class="img-responsive center-block" src="' + p_static_url + 'img/ajax_loader-small.gif">';


//    $(div_id).html(ajax_img);
//}

function display_loading_text(p_div_id, p_static_url) {
    var div_id = '#' + p_div_id;
    var ajax_img = '<p style="float: left;">Loading... <i class="fa fa-spinner fa-pulse"></i><p>';


    $(div_id).html(ajax_img);
}

function toggler(divId) {
    $("#" + divId).toggle();
}

function check_members_limits_callback (data) {
    var x_ratelimit_remaining = data.x_ratelimit_remaining;
    var x_ratelimit = data.x_ratelimit;
    var x_limit_pct = data.x_limit_pct;
    var likes_in_last_minute = data.likes_in_last_minute;
    var comments_in_last_minute = data.comments_in_last_minute;

    $('#ltm').html(likes_in_last_minute);
    $('#ctm').html(comments_in_last_minute);
    //$('#iglu').html(x_limit_pct + ' %');
}

function scroll_to_id(p_id) {
    var div_id = "#" + p_id;
    $('html, body').animate({
        scrollTop: $(div_id).offset().top - 50
    }, 600);
}

function check_members_limits() {
    Dajaxice.members.check_members_limits(check_members_limits_callback,
        {}
    );
}
check_members_limits();
setInterval(check_members_limits, 60 * 1000); // 60 * 1000 miliseconds

function status_bar_help() {
    $('#StatusBarHelpDialog').modal('show');
}

function show_div(p_div_id) {
    $('#' + p_div_id).fadeIn();
}

function dismiss_help_callback(data) {

}

function dismiss_help(p_help_name) {
    //alert('dismiss_help');

    Dajaxice.members.dismiss_help(dismiss_help_callback,
        {'p_help_name': p_help_name }
    );

}


function bootstrap_loading_button(p_button_id) {

    $('#' + p_button_id).button('loading');


}

function bootstrap_loading_reset(p_button_id) {
    $('#' + p_button_id).button('reset');
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})