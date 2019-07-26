$(document).ready(function () {
  $('#caller_id_mode').on('change', function () {
    toggle_callerid_mode.call(this)
  });
  toggle_callerid_mode.call($('#caller_id_mode'));

  var selectors = [
    '#fallbacks-noanswer_destination-queue-queue_id',
    '#fallbacks-noanswer_destination-queue-skill_rule_id',
  ];
  var $selects = {};
  var ids = {};
  for (var i = 0; i < selectors.length; i++) {
    var $select = $(selectors[i]);
    var listingUrl = $select.data('listing_href') || $select.data('listing-href');
    var id = $select.val();
    $selects[i] = $select;
    ids[i] = id;
    if (!id) {
      continue;
    }

    $select.empty();

    $.ajax({ url: listingUrl, idx : i, success: function(data) {
      var $select = $selects[this.idx];
      var id = ids[this.idx];
      $.each(data.results, function(idx, result) {
        $select.append($("<option></option>").attr('value', result.id).text(result.text));
      });
      $select.val(id);

      $select.select2({
        theme: 'bootstrap',
        placeholder: 'Select...',
      });
    }});
  }
});

function toggle_callerid_mode() {
  if ($(this).val() === '') {
    $('#caller_id_name').closest('div.form-group').hide()
  } else {
    $('#caller_id_name').closest('div.form-group').show()
  }
}
