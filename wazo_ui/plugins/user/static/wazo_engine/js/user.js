$(document).ready(function() {
  create_list_table();
  init_add_available_extensions.call(this);
  init_toggle_template_disable.call(this);

  // Remove spaces in email
  var removeSpace = function() {
    $(this).val($(this).val().replace(/\s/g, ''));
  };
  $(".modal-content #email, #user #username").keyup(removeSpace).blur(removeSpace).keypress(removeSpace);

  $('.row-template').on("row:cloned", function(e, row) {
    init_add_available_extensions.call(row);
    init_toggle_template_disable.call(row);
  });

  $('.row-line').each(function(e, row) {
    add_available_extensions.call(row);
    toggle_template_disable.call(row);
  });

  toggle_busy_destination_validator();
  $('#forwards-busy-enabled').change(toggle_busy_destination_validator);
  toggle_noanswer_destination_validator();
  $('#forwards-noanswer-enabled').change(toggle_noanswer_destination_validator);
  toggle_unconditional_destination_validator();
  $('#forwards-unconditional-enabled').change(toggle_unconditional_destination_validator);

  // Handle all destinations
  var selects = $('select').filter(function() {
    return this.id.match(/funckeys-[0-9]+-destination-queue-queue_id/)
      || this.id.match(/funckeys-[0-9]+-destination-group-group_id/)
      || this.id.match(/funckeys-[0-9]+-destination-groupmember-group_id/);
  });
  var $selects = {};
  var ids = {};
  for (var i = 0; i < selects.length; i++) {
    var $select = $(selects[i]);
    var listingUrl = $select.data('listing-href');
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
        theme: 'bootstrap4',
        placeholder: 'Select...',
      });
    }});
  }
});


function create_list_table() {
  var table_config = {
    columns: [
      { data: 'firstname' },
      { data: 'lastname' },
      { data: 'email' },
      { data: 'extension' },
      { data: 'provisioning_code' },
    ]
  };
  create_table_serverside(table_config);
}

function toggle_busy_destination_validator() {
    if ($('#forwards-busy-enabled').is(":checked")) {
      $('#forwards-busy-destination').attr('required', 'required');
    } else {
      $('#forwards-busy-destination').removeAttr('required');
    }
    $('form').validator('update');
    $('form').validator('validate');
}

function toggle_noanswer_destination_validator() {
    if ($('#forwards-noanswer-enabled').is(":checked")) {
      $('#forwards-noanswer-destination').attr('required', 'required');
    } else {
      $('#forwards-noanswer-destination').removeAttr('required');
    }
    $('form').validator('update');
    $('form').validator('validate');
}

function toggle_unconditional_destination_validator() {
    if ($('#forwards-unconditional-enabled').is(":checked")) {
      $('#forwards-unconditional-destination').attr('required', 'required');
    } else {
      $('#forwards-unconditional-destination').removeAttr('required');
    }
    $('form').validator('update');
    $('form').validator('validate');
}

function init_add_available_extensions(){
  $('.line-context', this).on("select2:select", function(e) {
    add_available_extensions.call(this);
  });
  add_available_extensions()
}


function add_available_extensions() {
  let extension_select, context_select;

  if ($('.row-template').length === 0) {
    extension_select = $(".line-extension");
    context_select = $(".line-context");
  } else {
    extension_select = $(this).closest("tr").find(".line-extension");
    context_select = $(this).closest("tr").find(".line-context");

    if (extension_select.length === 0) {
      extension_select = $(this).closest("form").find(".line-extension");
    }
  }

  let ajax_url = $(extension_select).attr('data-listing-href');
  if (! ajax_url || ! context_select) {
    return;
  }

  extension_select.select2({
    allowClear: true,
    theme: 'bootstrap4',
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

function init_toggle_template_disable(){
  $('.line-protocol', this).on("select2:select", function(e) {
    toggle_template_disable.call(this);
  });
  toggle_template_disable()
}

function toggle_template_disable() {
  let protocol_select, template_select;

  if ($('.row-template').length === 0) {
    protocol_select = $(".line-protocol");
    template_select = $(".line-template");
  } else {
    protocol_select = $(this).closest("tr").find(".line-protocol");
    template_select = $(this).closest("tr").find(".line-template");
  }

  if (protocol_select.val() == 'sip') {
    $(template_select).removeAttr('disabled');
  } else {
    $(template_select).attr('disabled', 'disabled');
  }
}
