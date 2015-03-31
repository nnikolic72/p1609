/**
 * Created by tanja on 3/29/2015.
 */

function import_instagram_followings_callback(data) {
    var instagram_followings_placeholder = '#instagram_followings_placeholder';
    var html_text = data.html_text;

    //alert('import_instagram_followings_callback ');
    $(instagram_followings_placeholder).html(html_text);
}

function import_instagram_followings(p_instagram_user_id) {
    //alert('import_instagram_followings ' + p_instagram_user_id);

    Dajaxice.smartfeed.import_instagram_followings(import_instagram_followings_callback,
        {'p_instagram_user_id': p_instagram_user_id}
    );

}

function smart_feed_subscribe_callback(data) {
    //alert('smart_feed_subscribe_callback');
    var action_result = data.action_result;
    var p_instagram_user_id = data.p_instagram_user_id;
    var p_color = data.p_color;
    var button_id = '#';

    if (action_result == 1) {
        if(p_color == 'green') {
            button_id += 'smartfeed_g_' +  p_instagram_user_id;
            $(button_id).removeClass('btn-default').addClass('btn-success');
        }
        if(p_color == 'yellow') {
            button_id += 'smartfeed_y_' +  p_instagram_user_id;
            $(button_id).removeClass('btn-default').addClass('btn-success');
        }
        if(p_color == 'red') {
            button_id += 'smartfeed_r_' +  p_instagram_user_id;
            $(button_id).removeClass('btn-default').addClass('btn-success');
        }
    }

}

function smart_feed_subscribe(p_instagram_user_id, p_color) {
    //alert('smart_feed_subscribe ' + p_instagram_user_id + ' ' + p_color);

    Dajaxice.smartfeed.smart_feed_subscribe(smart_feed_subscribe_callback,
        {'p_instagram_user_id': p_instagram_user_id, 'p_color': p_color}
    );
}