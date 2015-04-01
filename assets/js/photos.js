/**
 * Created by n.nikolic on 3/25/2015.
 */

function save_attributes_and_categories_callback(data) {
    //alert('save_attributes_and_categories_callback');
    var modal_name = data.modal_name;

    //alert(modal_name);
    $(modal_name).modal('toggle');
}

function save_attributes_and_categories(p_photo_id) {
    // alert('save_attributes_and_categories');
    id_name = '#category_selection_form_' + p_photo_id;
    var data = $(id_name).serializeObject();
    //alert(data);
    Dajaxice.photos.save_attributes_and_categories(save_attributes_and_categories_callback,
        {'form': data, 'p_photo_id': p_photo_id}
    );
}

function show_comments_modal(p_photo_id) {

    var modal_name = '#myModal_comments_' + p_photo_id;

    //alert('Show modal: ' + modal_name);
    $(modal_name).modal('show');
}

function hide_comments_modal(p_photo_id) {

    var modal_name = '#myModal_comments_' + p_photo_id;

    //alert('Show modal: ' + modal_name);
    $(modal_name).modal('hide');
}

function load_instagram_comments_callback(data) {
    //alert('load_instagram_comments_callback');
    var p_photo_id = data.p_photo_id;
    var html_text = data.html_text;

    //alert(html_text);
    var modal_comment_text_id = '#myModal_comments_text_' + p_photo_id;

    $(modal_comment_text_id).html(html_text)


    show_comments_modal(p_photo_id);


}

function load_instagram_comments(p_photo_id) {
    //alert('load_instagram_comments');
    Dajaxice.photos.load_instagram_comments(load_instagram_comments_callback,
        {'p_photo_id': p_photo_id}
    );
}

function send_instagram_comment_callback(data) {
    //alert('send_instagram_comment_callback');
    var p_photo_id = data.p_photo_id;
    var x_limit_pct = data.x_limit_pct;
    var comments_per_minute = data.comments_per_minute;

    $('#iglu').html(x_limit_pct);
    $('#cpm').html(comments_per_minute);
    var l_comments_count = data.l_comments_count;

    var instagram_comments_text_id = '#instagram_comments_text_' + p_photo_id;
    $(instagram_comments_text_id).html(l_comments_count);
    load_instagram_comments(p_photo_id);
    //show_comments_modal(p_photo_id); //hides
}

function send_instagram_comment(p_photo_id) {
    //alert('send_instagram_comment ' + p_photo_id);
    var id_name = '#comment_form_' + p_photo_id;
    var data = $(id_name).serializeObject();

    //alert('send_instagram_comment ' + data);

    Dajaxice.photos.send_instagram_comment(send_instagram_comment_callback,
        {'form': data, 'p_photo_id': p_photo_id, 'p_inline': '' }
    );
}

function send_instagram_inline_comment(p_photo_id, p_comment_order) {
    //alert('send_instagram_inline_comment ' + p_photo_id);
    var id_name = '#inline_comment_form_' + p_photo_id + '_' + p_comment_order;
    var data = $(id_name).serializeObject();
    //alert('send_instagram_inline_comment ' + p_photo_id + 'exit');
    alert('send_instagram_inline_comment ' + data);

    Dajaxice.photos.send_instagram_comment(send_instagram_comment_callback,
        {'form': data, 'p_photo_id': p_photo_id, 'p_inline': p_comment_order  }
    );
}


function like_instagram_picture_callback(data) {
    //alert('like_instagram_picture_callback');
    var result = data.result;
    var p_photo_id = data.p_photo_id;
    var no_of_likes = data.no_of_likes;
    var button_id = '#like_button_' + p_photo_id;
    var ig_likes_text_id = '#instagram_likes_text_' + p_photo_id;


    if(result=='like') {
        $(button_id).removeClass('btn-default').addClass('btn-danger');
    }

    if(result=='unlike') {
        $(button_id).removeClass('btn-danger').addClass('btn-default');
    }

    $(ig_likes_text_id).html(no_of_likes)
}

function like_instagram_picture(p_photo_id) {
    //alert('like_instagram_picture');
    // var id_name = '#comment_form_' + p_photo_id;
    // var data = $(id_name).serializeObject();

    //alert('send_instagram_comment ' + data);

    Dajaxice.photos.like_instagram_picture(like_instagram_picture_callback,
        { 'p_photo_id': p_photo_id }
    );
}
