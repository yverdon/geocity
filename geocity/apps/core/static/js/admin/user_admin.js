// Edit css class for selectors (group and permissions)
// They're by default at col-sm-7 and aren't readable cause the box is too small

window.addEventListener('load', function () {
    var selector = document.getElementsByClassName("col-sm-7 field-user_permissions").item(0);
    selector.className="col-sm-12";

    var selector = document.getElementsByClassName("col-sm-7 field-groups").item(0);
    selector.className="col-sm-12";
})
