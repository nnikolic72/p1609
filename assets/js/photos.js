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
    var p_new_friends_interaction = data.p_new_friends_interaction;

    //alert(html_text);
    var modal_comment_text_id = '#myModal_comments_text_' + p_photo_id;

    $(modal_comment_text_id).html(html_text);

    bootstrap_loading_reset('send_comment_' + p_photo_id);
    show_comments_modal(p_photo_id);


}

function load_instagram_comments(p_photo_id, p_new_friends_interaction) {
    //alert('load_instagram_comments');
    p_new_friends_interaction = typeof p_new_friends_interaction !== 'undefined' ? p_new_friends_interaction : 0;

    Dajaxice.photos.load_instagram_comments(load_instagram_comments_callback,
        {'p_photo_id': p_photo_id, 'p_new_friends_interaction': p_new_friends_interaction}
    );
}

function show_hidden_comments(p_photo_id) {
    $('#hidden-comments_' + p_photo_id).show();
}

function send_instagram_comment_callback(data) {
    //alert('send_instagram_comment_callback');
    var p_photo_id = data.p_photo_id;
    var p_new_friends_interaction = data.p_new_friends_interaction;
    var p_photo_author_instagram_id = data.p_photo_author_instagram_id;
    var comments_per_minute = data.comments_per_minute;
    var x_limit_pct = data.x_limit_pct.toPrecision(2);
    var result = data.result;
    var interactions_remaining = data.interactions_remaining;

    var l_comments_count = data.l_comments_count;

    var instagram_comments_text_id = '#instagram_comments_text_' + p_photo_id;
    $(instagram_comments_text_id).html(l_comments_count);

    if(result=='limit') {
        hide_comments_modal(p_photo_id);
        $('#error-message').html('Comment not sent. You have hit the hourly limit in commenting the posts. Please wait and try again later.');
        $('#ErrorDialog').modal('show');
    } else {
        if (p_new_friends_interaction == 0) {

            load_instagram_comments(p_photo_id);
        }

        if (p_new_friends_interaction == 1) {
            var new_friend_id = "#new_friend_" + p_photo_author_instagram_id;
            hide_comments_modal(p_photo_id);
            $('html, body').animate({
                scrollTop: $(new_friend_id).offset().top - 50
            }, 600);
            $(new_friend_id).hide();

            $('#interactions_remaining_text').html(interactions_remaining);
        }
    }

    if(result != 'error') {
        $('#ctm').html(comments_per_minute);
        $('#iglu').html(x_limit_pct + ' %');
    }


    //if we interact with new friends -
    //show_comments_modal(p_photo_id); //hides
}

function send_instagram_comment(p_photo_id, p_new_friends_interaction) {
    //alert('send_instagram_comment ' + p_photo_id);
    var id_name = '#comment_form_' + p_photo_id;
    var data = $(id_name).serializeObject();

    //alert('send_instagram_comment ' + data);

    bootstrap_loading_button('send_comment_' + p_photo_id);

    Dajaxice.photos.send_instagram_comment(send_instagram_comment_callback,
        {'form': data, 'p_photo_id': p_photo_id, 'p_inline': '',
            'p_new_friends_interaction': p_new_friends_interaction
        }
    );
}

function send_instagram_inline_comment(p_photo_id, p_comment_order) {
    //alert('send_instagram_inline_comment ' + p_photo_id);
    var id_name = '#inline_comment_form_' + p_photo_id + '_' + p_comment_order;
    var data = $(id_name).serializeObject();
    //alert('send_instagram_inline_comment ' + p_photo_id + 'exit');
    //alert('send_instagram_inline_comment ' + data);
    bootstrap_loading_button('inline_comment_' + p_photo_id + '_' + p_comment_order);

    Dajaxice.photos.send_instagram_comment(send_instagram_comment_callback,
        {'form': data, 'p_photo_id': p_photo_id, 'p_inline': p_comment_order,
        'p_new_friends_interaction': 0 }
    );
}


function like_instagram_picture_callback(data) {
    //alert('like_instagram_picture_callback');
    var result = data.result;
    var p_photo_id = data.p_photo_id;
    var no_of_likes = data.no_of_likes;
    var likes_per_minute = data.likes_per_minute;
    var x_limit_pct = data.x_limit_pct.toPrecision(2);

    var button_id = '#like_button_' + p_photo_id;
    var ig_likes_text_id = '#instagram_likes_text_' + p_photo_id;
    var html_text = '';

    var current_likes_cnt = data.current_likes_cnt;


    if(result=='like') {
        $(button_id).removeClass('btn-default').addClass('btn-danger');
        current_likes_cnt++;
    }

    if(result=='unlike') {
        $(button_id).removeClass('btn-danger').addClass('btn-default');
        current_likes_cnt--;
    }

    if(result=='limit') {
        $('#error-message').html('Like not sent. You have hit the hourly limit in liking the posts. Please wait and try again later.');
        $('#ErrorDialog').modal('show');
    }

    html_text += '<small><span class="glyphicon glyphicon-heart-empty"></span>';
    html_text += '&nbsp;<div class="badge" id="instagram_likes_text_'+ p_photo_id + '">' + current_likes_cnt + '</div></small>';
    $(button_id).html(html_text);

    $('#ltm').html(likes_per_minute);
    $('#iglu').html(x_limit_pct + ' %');
}

function like_instagram_picture(p_photo_id, p_static_url) {
    //alert('like_instagram_picture');
    // var id_name = '#comment_form_' + p_photo_id;
    // var data = $(id_name).serializeObject();
    var ig_likes_text_id = '#instagram_likes_text_' + p_photo_id;
    var current_likes_cnt = parseInt($(ig_likes_text_id).text(), 10);
    var button_id = '#like_button_' + p_photo_id;
    //var html_text = '<div align=center><img class="img-responsive" src="' + p_static_url + 'img/ajax_loader-small.gif" style="height=11px;"></div>';
    var html_text = '<i class="fa fa-spinner fa-pulse"></i>';

    $(button_id).removeClass('btn-danger');
    $(button_id).html(html_text);
    //alert('send_instagram_comment ' + data);


    Dajaxice.photos.like_instagram_picture(like_instagram_picture_callback,
        { 'p_photo_id': p_photo_id, 'current_likes_cnt': current_likes_cnt }
    );
}

function add_response_username(p_username, p_photo_id) {
    var textarea_id = '#' + 'response_' + p_photo_id;

    var textarea_value = $(textarea_id).val();

    textarea_value += '@' + p_username + ' ';
    $(textarea_id).val(textarea_value);
}


function load_instagram_commenter_comments_callback(data) {
    //alert('load_instagram_commenter_comments_callback');
    var p_photo_id = data.p_photo_id;
    var html_text = data.html_text;
    //var p_new_friends_interaction = data.p_new_friends_interaction;

    //alert(html_text);
    var modal_comment_text_id = '#commenter_photo_block_' + p_photo_id;
    var send_response_button_id = '#send_instagram_commenter_comment_' + p_photo_id;
    var response_textarea_id = '#response_' + p_photo_id;

    $(modal_comment_text_id).html(html_text);
    //$(send_response_button_id).html('Send Response');
    bootstrap_loading_reset('send_instagram_commenter_comment_' + p_photo_id);
    $(response_textarea_id).val('');

    toggler('comments_' + p_photo_id);
    if($('#' + 'comments_' + p_photo_id).length == 0) {
        //it doesn't exist
        scroll_to_id('commenter_comment_block');
    } else {
        scroll_to_id('commenter_photo_block_' + p_photo_id);
    }
}

function load_instagram_commenter_comments(p_photo_id) {
    //alert('load_instagram_commenter_comments');
    //p_new_friends_interaction = typeof p_new_friends_interaction !== 'undefined' ? p_new_friends_interaction : 0;

    Dajaxice.photos.load_instagram_commenter_comments(load_instagram_commenter_comments_callback,
        {'p_photo_id': p_photo_id}
    );
}

function send_instagram_commenter_comment_callback(data) {
    //alert('send_instagram_commenter_comment_callback');
    var p_photo_id = data.p_photo_id;
    var p_photo_author_instagram_id = data.p_photo_author_instagram_id;
    var comments_per_minute = data.comments_per_minute;
    var x_limit_pct = data.x_limit_pct.toPrecision(2);
    var result = data.result;

    if(result=='limit') {
        //hide_comments_modal(p_photo_id);
        $('#error-message').html('Comment not sent. You have hit the hourly limit in commenting the posts. Please wait and try again later.');
        $('#ErrorDialog').modal('show');
    } else {
        // Reload comments here
        load_instagram_commenter_comments(p_photo_id);
    }

    $('#ctm').html(comments_per_minute);
    $('#iglu').html(x_limit_pct + ' %');



}

function send_instagram_commenter_comment(p_photo_id, p_static_url) {
    //alert('send_instagram_commenter_comment ' + p_photo_id);
    var id_name = '#comment_form_' + p_photo_id;
    var data = $(id_name).serializeObject();

    var comment_text = $('#response_' + p_photo_id).val();
    //display_ajax_img('send_instagram_commenter_comment_' + p_photo_id, p_static_url);
    bootstrap_loading_button('send_instagram_commenter_comment_' + p_photo_id);

    //alert('send_instagram_comment ' + data);

    Dajaxice.photos.send_instagram_commenter_comment(send_instagram_commenter_comment_callback,
        {'form': data, 'p_photo_id': p_photo_id, 'p_comment_text': comment_text}
    );
}