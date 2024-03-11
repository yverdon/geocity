// Get all messages of the alert-success class
let info_messages = document.getElementsByClassName('alert-success');

setTimeout(function(){
    for (let i = 0; i < info_messages.length; i ++) {
        info_messages[i].setAttribute('style', 'display:none');
    }
}, 4000);
