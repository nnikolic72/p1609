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