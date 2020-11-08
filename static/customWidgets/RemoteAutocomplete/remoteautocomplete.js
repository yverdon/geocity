
$( function() {

  $('[data_remote_autocomplete]').each(function(index, item){

    $("#" + item.id ).autocomplete({

        classes: {
            "ui-autocomplete": "sit-autocomplete"
        },
        source: function( request, response ) {

            var dataRemoteAutocomplete = jQuery.parseJSON($("#" + item.id ).attr('data_remote_autocomplete'))

            $.ajax({
                url: dataRemoteAutocomplete.apiurl,
                dataType: "json",
                data: {
                    searchText: request.term,
                    limit: 20,
                    partitionlimit: 24,
                    type: 'locations',
                    sr: 2056,
                    lang: 'fr',
                    origins: dataRemoteAutocomplete.origins
                },
                success: function(data) {
                    let features = data.results;
                    let items = [];
                    for(let i=0; i<features.length; i++) {
                        let f = features[i];
                        let item = {
                            x: f.attrs.x,
                            y: f.attrs.y,
                            id: f.attrs.featureId,
                            label: f.attrs.label.replace('<b>', ' - ').replace('</b>',''),
                            value: f.attrs.detail,
                        }
                        items.push(item)
                    }
                    response(items);
                }
            });
        },
        minLength: 2,
        select: function(event, ui) {

            var dataRemoteAutocomplete = jQuery.parseJSON($("#" + item.id ).attr('data_remote_autocomplete'))
            $.ajax({
                url: dataRemoteAutocomplete.apiurl_detail +  ui.item.id,
                dataType: "json",
                data: {
                    returnGeometry: false
                },
                success: function(data) {
                  var nmr = data.feature.attributes.deinr;
                  if (nmr == null) {
                    nmr = '';
                  }
                  var formPrefix = event.target.attributes.id.value.substring(0,9);
                  $("#" + item.id ).val(data.feature.attributes.strname + ' ' + nmr);
                  if (dataRemoteAutocomplete.zipcode_field != "") {
                      var field = '#' + formPrefix + '-' + dataRemoteAutocomplete.zipcode_field;
                      $(field).val(data.feature.attributes.dplz4);
                  }
                  if (dataRemoteAutocomplete.city_field != "") {
                      var field = '#' + formPrefix + '-' + dataRemoteAutocomplete.city_field;
                      $(field).val(data.feature.attributes.dplzname);
                  }
                }
            });
        }
    });

  })

});
