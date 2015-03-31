/**
 * Created by tanja on 3/29/2015.
 */

function import_instagram_followings_callback(data) {
    var l_instagram_followings = data.l_instagram_followings;

    alert('import_instagram_followings_callback ');
}

function import_instagram_followings(p_instagram_user_id) {
    alert('import_instagram_followings ' + p_instagram_user_id);

    Dajaxice.smartfeed.import_instagram_followings(import_instagram_followings_callback,
        {'p_instagram_user_id': p_instagram_user_id}
    );

}