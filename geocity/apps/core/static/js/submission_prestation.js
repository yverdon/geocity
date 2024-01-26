const updateFormMonetaryAmount = () => {
  var serviceFeeType = document.getElementById("select2-id_service_fee_type-container");
  let monetaryAmount = document.getElementById("id_monetary_amount");
  let jsonstr = JSON.parse(document.getElementById("get-data").textContent);
  if (!jsonstr) {
    return;
  }
  let json = JSON.parse(jsonstr);
  if (monetaryAmount) {
    json.forEach((item) => {
      if (item.name === serviceFeeType.title) {
        monetaryAmount.value = item.fix_price
        if (item.fix_price_editable ) {
          monetaryAmount.readOnly = false;
        } else {
          monetaryAmount.readOnly = true;
        }
      }
    });
  }
};
