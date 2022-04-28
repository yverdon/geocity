$(function () {
  $("[data_remote_autocomplete]").each(function (index, item) {
    var itemId = $("#" + item.id);
    itemId.autocomplete({
      classes: {
        "ui-autocomplete": "sit-autocomplete",
      },
      source: function (request, response) {
        var dataRemoteAutocomplete = jQuery.parseJSON(
          itemId.attr("data_remote_autocomplete")
        );
        var additionalSearchtext = itemId.attr("additional_searchtext_for_address_field");
        if(additionalSearchtext) {
          request.term += ' ' + additionalSearchtext;
        }

        $.ajax({
          url: dataRemoteAutocomplete.apiurl,
          dataType: "json",
          data: {
            searchText: request.term,
            limit: 20,
            partitionlimit: 24,
            type: "locations",
            sr: 2056,
            lang: "fr",
            origins: dataRemoteAutocomplete.origins,
          },
          success: function (data) {
            let features = data.results;
            let items = [];
            for (let i = 0; i < features.length; i++) {
              let f = features[i];
              let item = {
                x: f.attrs.x,
                y: f.attrs.y,
                id: f.attrs.featureId,
                label: f.attrs.label.replace(/\s\<b\>\s*/g, ", ").replace(/\s*[\<\(][^\)\>]*[\)\>]*/g, ""),
                value: f.attrs.detail,
              };
              items.push(item);
            }
            response(items);
          },
        });
      },
      minLength: 2,
      select: function (event, ui) {
        var dataRemoteAutocomplete = jQuery.parseJSON(
          itemId.attr("data_remote_autocomplete")
        );
        if (dataRemoteAutocomplete.is_address) {
          $.ajax({
            url: dataRemoteAutocomplete.apiurl_detail + ui.item.id,
            dataType: "json",
            data: {
              returnGeometry: false,
            },
            success: function (data) {
              var nmr = data.feature.attributes.deinr;
              var street = "";
              if (nmr == null || nmr === "") {
                street = data.feature.attributes.strname.join(" ");
              } else {
                street = data.feature.attributes.strname.join(" ") + " " + nmr;
              }
              var formPrefix = event.target.attributes.id.value.substring(0, 9);
              item.value = street;
              if (
                dataRemoteAutocomplete.single_address_field
              ) {
                item.value = street + ", " + data.feature.attributes.dplz4 + " " + data.feature.attributes.dplzname;
                return;
              }
              if (
                dataRemoteAutocomplete.zipcode_field != "" &&
                !dataRemoteAutocomplete.single_contact
              ) {
                var field =
                  "#" + formPrefix + "-" + dataRemoteAutocomplete.zipcode_field;
                $(field).val(data.feature.attributes.dplz4);
              } else {
                $("#id_" + dataRemoteAutocomplete.zipcode_field).val(
                  data.feature.attributes.dplz4
                );
              }
              if (
                dataRemoteAutocomplete.city_field != "" &&
                !dataRemoteAutocomplete.single_contact
              ) {
                var field =
                  "#" + formPrefix + "-" + dataRemoteAutocomplete.city_field;
                $(field).val(data.feature.attributes.dplzname);
              } else {
                $("#id_" + dataRemoteAutocomplete.city_field).val(
                  data.feature.attributes.dplzname
                );
              }
            },
          });
        }
        else {
          item.value = ui.item.label;
        }
        return false;
      },
    });
  });
});
