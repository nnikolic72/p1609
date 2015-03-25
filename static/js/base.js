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