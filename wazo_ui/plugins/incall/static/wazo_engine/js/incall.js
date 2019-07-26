$(document).ready(function () {
  $('.incall-context').on("change", function (e) {
    add_available_extensions();
  });

  var $mode = $('#caller_id_mode');
  add_available_extensions();
  $mode.on('change', function (e) {
    toggle_callerid_mode.call(this)
  });
  toggle_callerid_mode.call($mode);
});


function toggle_callerid_mode() {
  var $name = $('#caller_id_name');

  if ($(this).val() === '') {
    $name.closest('div.form-group').hide();
  } else {
    $name.closest('div.form-group').show();
  }
}


function add_available_extensions() {
  let extension_select = $(".incall-exten");
  let context_select = $(".incall-context");
  let ajax_url = $(extension_select).attr('data-listing-href') || $(extension_select).attr('data-listing_href');
  if (!ajax_url) {
    return;
  }

  extension_select.select2({
    theme: 'bootstrap',
    placeholder: 'Select...',
    tags: true,
    ajax: {
      url: ajax_url,
      data: function (params) {
        return {
          term: params.term,
          context: context_select.val()
        }
      }
    }
  });
}

$(document).ready(function() {
  var selectors = ['#destination-queue-skill_rule_id', '#destination-queue-queue_id'];
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
