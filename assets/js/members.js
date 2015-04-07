/**
 * Created by n.nikolic on 3/25/2015.
 */

function select_member_category_callback(data) {
    //alert('select_member_category_callback');

    var p_category_id = data.p_category_id;
    var p_result = data.p_result;
    var button_id = '#category_button_' + p_category_id;

    if (p_result=='add') {
        $(button_id).removeClass('btn-default').addClass('btn-info');
    }

    if (p_result=='remove') {
        $(button_id).removeClass('btn-info').addClass('btn-default');
    }
}

function select_member_category(p_category_id, p_logged_member_id) {
    //alert('select_member_category');

    Dajaxice.members.select_member_category(select_member_category_callback,
        {'p_category_id': p_category_id, 'p_logged_member_id': p_logged_member_id}
    );
}




function select_member_attribute_callback(data) {
    //alert('select_member_attribute_callback');

    var p_attribute_id = data.p_attribute_id;
    var p_result = data.p_result;
    var button_id = '#attribute_button_' + p_attribute_id;

    if (p_result=='add') {
        $(button_id).removeClass('btn-default').addClass('btn-info');
    }

    if (p_result=='remove') {
        $(button_id).removeClass('btn-info').addClass('btn-default');
    }
}

function select_member_attribute(p_attribute_id, p_logged_member_id) {
    //alert('select_member_attribute');

    Dajaxice.members.select_member_attribute(select_member_attribute_callback,
        {'p_attribute_id': p_attribute_id, 'p_logged_member_id': p_logged_member_id}
    );
}

