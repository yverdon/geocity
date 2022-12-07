(function() {
  var statusChangeBtns = document.getElementsByClassName("transactionStatusChangeBtn")

  for (let item of statusChangeBtns) {
    item.addEventListener("click", event => {
      event.preventDefault();
      var merchantRef = event.target.getAttribute("data-merchant-reference")
      var url = event.target.getAttribute("data-href")
      var select = document.getElementById("transactionStatusChangeSelect-" + merchantRef);
      var value = select.options[select.selectedIndex].value;
      if (value !== "") {
        window.location.href = url + "?new_status=" + value;
      }
    })
  }
})();
