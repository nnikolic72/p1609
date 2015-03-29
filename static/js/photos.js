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
    $(modal_name).modal('toggle');
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
    alert('send_instagram_comment_callback');
    var p_photo_id = data.p_photo_id;
    show_comments_modal(p_photo_id); //hides
}

function send_instagram_comment(p_photo_id) {
    //alert('send_instagram_comment ' + p_photo_id);
    var id_name = '#comment_form_' + p_photo_id;
    var data = $(id_name).serializeObject();

    //alert('send_instagram_comment ' + data);

    Dajaxice.photos.send_instagram_comment(send_instagram_comment_callback,
        {'form': data, 'p_photo_id': p_photo_id }
    );
}