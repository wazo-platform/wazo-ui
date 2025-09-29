$(document).ready(function () {
  init_time_picker.call(this);

  $('.row-template').on('row:cloned', function (e, row) {
    init_time_picker.call(row);
  });
});

function init_time_picker() {
  $('[class^=schedule_date_hours_]', this).timepicker({
    'timeFormat': 'H:i',
    'step': function (i) {
      return (i % 2) ? 15 : 45;
    }
  });
}

$(document).ready(function() {
  var selectors = ['#closed_destination-queue-queue_id', '#closed_destination-queue-skill_rule_id'];
  var $selects = {};
  var ids = {};
  for (var i = 0; i < selectors.length; i++) {
    var $select = $(selectors[i]);
    var listingUrl = $select.data('listing_href') || $select.data('listing-href');
    var id = $select.val();
    $selects[listingUrl] = $select;
    ids[listingUrl] = id;
    if (!id) {
      continue;
    }

    $select.empty();

    $.ajax({ url: listingUrl, success: function(data) {
      var $select = $selects[this.url];
      var id = ids[this.url];
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
