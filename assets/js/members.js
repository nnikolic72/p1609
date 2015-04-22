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

function squaresensor_wizard_increase_step_callback(data) {

}

function squaresensor_wizard_callback(data) {
    //alert('squaresensor_wizard_callback');
    var p_current_step = data.p_current_step;
    var html_text = data.html_text;
    var p_instagram_user_id = data.p_instagram_user_id;

    $('#wizard-placeholder').fadeOut(600, function() {
            scroll_to_id('wizard-placeholder');
            $('#wizard-placeholder').html(html_text);
        }
    );

    $('#wizard-placeholder').fadeIn();

    Dajaxice.members.squaresensor_wizard_increase_step(squaresensor_wizard_increase_step_callback,
        {'p_current_step': p_current_step }
    );

    if (p_current_step == '3') {
        // Loading of instagram Followings
        import_instagram_followings(p_instagram_user_id);
    }
    //$('#wizard-placeholder').html(html_text);
    //$('#wizard-placeholder').fadeIn();
}


function squaresensor_wizard(p_current_step) {
    //alert('squaresensor_wizard, step ' + p_current_step );

    Dajaxice.members.squaresensor_wizard(squaresensor_wizard_callback,
        {'p_current_step': p_current_step}
    );

}

function squaresensor_wizard_complete_callback(data) {

}

function squaresensor_wizard_complete() {
    //alert('squaresensor_wizard_complete');

    Dajaxice.members.squaresensor_wizard_complete(squaresensor_wizard_complete_callback,
        {}
    );

}
