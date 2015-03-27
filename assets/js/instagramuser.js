/**
 * Created by tanja on 3/27/2015.
 */

function analyze_user_callback(data) {
    //alert('analyze_user_callback');
    var photos = data.photos;
    var already_exists = data.already_exists;
    var error = data.error;
    var error_message = data.error_message;
    var categories = data.categories;
    var attributes = data.attributes;
    var analyze_button = '#analyze_button';

    var id_bestphotos_div = '#bestphotos';
    $(analyze_button).html('Analyze');

    if (error == 1) {
        $(id_bestphotos_div).html('<p>' + error_message + '</p>');
    }

    var bestphotos_div_html = '';
    if (error == 0) {
        var photo_array_length = photos.length;
        for (var i = 0; i < photo_array_length; i++) {
            bestphotos_div_html += '<p><img class="img-responsive img-thumbnail" src="'
            + photos[i] + '"></p>';
            //bestphotos_div_html += '<p>'+ photo + '</p>';
        }

    }
    $(id_bestphotos_div).html(bestphotos_div_html)
}

function analyze_user() {
    //alert('analyze_user');
    var id_name = '#username';
    var analyze_button = '#analyze_button';
    //alert(id_name);
    var data = $(id_name).serializeObject();


    $(analyze_button).html('Analyzing...');
    //alert(data);
    Dajaxice.instagramuser.analyze_user(analyze_user_callback, {'form': data});

}