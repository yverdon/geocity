const updateFormMonetaryAmount = () => {
  var serviceFeeType = document.getElementById("select2-id_services_fees_type-container");
  let monetaryAmount = document.getElementById("id_monetary_amount_0");
  let jsonstr = JSON.parse(document.getElementById("get-data").textContent);
  let json = JSON.parse(jsonstr);
  json.forEach((item) => {
    if (item.name === serviceFeeType.title) {
      monetaryAmount.value = item.fix_price
    }
  });
};
