// Edit css class for selectors (group and permissions)
// They're by default at col-sm-7 and aren't readable cause the box is too small

window.addEventListener('load', function () {
    var selects = document.querySelectorAll('select')
    for (select of selects) {
        let div = select.closest('.col-sm-7')
        div.className="col-sm-12";
    }
});
