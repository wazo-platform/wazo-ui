$(document).ready(function() {
  var selectors = [
    '#invalid_destination-queue-queue_id',
    '#invalid_destination-queue-skill_rule_id',
    '#timeout_destination-queue-queue_id',
    '#timeout_destination-queue-skill_rule_id',
    '#abort_destination-queue-queue_id',
    '#abort_destination-queue-skill_rule_id',
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
