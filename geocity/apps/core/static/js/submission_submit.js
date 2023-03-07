const button = document.getElementById("btn_accept_terms");
const checkbox = document.getElementById("chk_accept_terms");
var message = document.getElementsByClassName("maximum-submission-message");

checkbox.addEventListener("click", () => {
    // Toggle the disable attribute only when there's no message for maximum-submission-message
    if (message.length == 0) {
        button.toggleAttribute("disabled");
    }
});
