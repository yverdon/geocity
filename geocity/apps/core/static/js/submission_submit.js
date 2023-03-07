const button = document.getElementById("btn_accept_terms");
const checkbox = document.getElementById("chk_accept_terms");
const message = document.getElementByClassName("maximum-submission-message");

checkbox.addEventListener("click", () => {
    // Toggle the disable attribute based on message visible or not
    if (!message) {
        button.toggleAttribute("disabled");
    }
});
