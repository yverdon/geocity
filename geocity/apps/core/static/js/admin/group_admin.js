// Edit css class for selectors (group and permissions)
// They're by default at col-sm-7 and aren't readable cause the box is too small

window.addEventListener('load', function () {
    var selector = document.getElementsByClassName("col-sm-7 field-permissions").item(0);
    console.log(selector);
    selector.className="col-sm-12";
})
