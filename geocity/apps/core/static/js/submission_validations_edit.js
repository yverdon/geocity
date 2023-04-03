// Create a label to replace "readonly hidden select" readonly
window.addEventListener('load', function () {
  var selects = document.querySelectorAll("select[readonly][hidden]");
  for (select of selects) {
    let elem = document.createElement('label');
    let text = select.querySelector("option[selected]").text
    let div = select.closest('.col-md-9');

    elem.innerHTML = text;
    elem.classList.add('col-form-label', 'bold');
    div.appendChild(elem);
  }
});
