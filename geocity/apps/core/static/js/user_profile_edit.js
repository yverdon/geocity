const button = document.getElementById("user_profile_edit");
const checkbox = document.getElementById("chk_accept_policy");

checkbox.addEventListener("click", () => {
    button.toggleAttribute("disabled");
});

button.toggleAttribute("disabled");
