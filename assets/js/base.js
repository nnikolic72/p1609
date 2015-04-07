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

function display_ajax_img(p_div_id, p_static_url) {
    var div_id = '#' + p_div_id;
    var ajax_img = '<img class="img-responsive center-block" src="' + p_static_url + 'img/ajax_loader-small.gif">';


    $(div_id).html(ajax_img);
}

function display_loading_text(p_div_id, p_static_url) {
    var div_id = '#' + p_div_id;
    var ajax_img = '<p style="float: left;">Loading...<p>';


    $(div_id).html(ajax_img);
}