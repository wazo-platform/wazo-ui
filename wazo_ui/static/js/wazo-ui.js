$.extend(true, $.fn.dataTable.defaults, {
  lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
  pageLength: 20,
  order: [],
  autoWidth: false,
  responsive: true,
  searching: true,
  select: {
    style: 'os'
  },
  search: {
    smart: false
  },
  stateSave: true,
  columnDefs: [
    {
      targets:   0,
      responsivePriority: 1
    },
    {
      targets: -1,
      responsivePriority: 2
    },
    {
      targets: '_all',
      defaultContent: "-"
    },
    {
      targets: 'no-sort',
      orderable: false
    }
  ],
  dom: "<'row'<'col-sm-8'B><'col-sm-4'f>>" +
       "<'row'<'col-sm-12'tr>>" +
       "<'row'<'col-sm-5'il><'col-sm-7'p>>",
  buttons: [
    'selectAll',
    'selectNone'
  ],
  initComplete: function(oSettings, json) {
    $('select[name^=table-list]').select2({
      theme: 'bootstrap',
      tags: true
    });
  },
});

$.fn.validator.Constructor.INPUT_SELECTOR = ':input:not([type="hidden"], [type="submit"], [type="reset"],' +
  ' [disabled], button, .hidden :input, .select2-search__field)';

function concatHashToString(hash){
  var emptyStr = '';
  $.each(hash, function(index){
    emptyStr += ' ' + hash[index].name + '="' + hash[index].value + '"';
  });
  return emptyStr;
}

var tableInstances = [];

$(document).ready(function() {
  create_table_clientside();

  $('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    popout: true,
    btnCancelClass: 'hidden',
    btnOkClass: 'btn-xs btn-primary bg-green color-palette'
  });

  $("#working-tenant,#working-instance-tenant").on("change", function () {
    $(this).submit();
  });

  $('#error-details-show').click(function() {
    $('#error-details-show').hide();
    $('#error-details-hide').show();
  });

  $('#error-details-hide').click(function() {
    $('#error-details-show').show();
    $('#error-details-hide').hide();
  });

  $("div.alert-success").fadeOut(3000);

  init_destination_select.call(this);
  init_select2.call(this);
  $(':input[type=password]:not(.row-template :input, [data-toggle=password])').password();

  $('.add-row-entry').click(function(e) {
    e.preventDefault();
    clone_row.call(this)
  });

  // Update name/id of template row
  $('.row-template :input[id]').not(":button").each(function() {
    var template_id = $(this).attr('id').replace(/-\d{1,4}-/, '-template-');
    $(this).attr('name', template_id).attr('id', template_id);
  });

  $('.delete-row-entry').click(function(e) {
    e.preventDefault();
    $(this).closest("tr").remove();
    $(".row-template").trigger("row:deleted", $(this).closest("tr"));
  });

  //
  $('.btn-flat[data-loading-text]').click(function () {
    $(this).button('loading');
  });

  // Add breadcrumbs
  $('form.with-breadcrumbs').each(function(idx, form) {
    var $forms = $(form);
    $forms.attr('action', addCurrentBreadcrumbs($forms.attr('action')));
  });
  $('a.with-breadcrumbs').each(function(idx, link) {
    var $link = $(link);
    $link.attr('href', addCurrentBreadcrumbs($link.attr('href')));
  });

  // Add loader to button with .data-loading-text
  var button = $('[data-loading-text]');
  if (button.length) {
    var attributes = button[0].attributes;
    button.replaceWith($('<button '+ concatHashToString(attributes) +'>' + attributes.value.value + '</button>'));

    $('[data-loading-text]:not(.disabled)').on('click', function () {
      if($(this).hasClass('disabled')) {
        return;
      }

      $(this).button('loading');
    });
  }

  // Recalc datatables size after a tab change (useful for responsive tables)
  $('a[data-toggle="tab"]').on('shown.bs.tab', function () {
    $('table.client-side:visible').each(function() {
      var $this = $(this);
      var rowId = $this.attr('data-row-id');
      tableInstances[rowId].columns.adjust().responsive.recalc();
    });
  });
});


function clone_row() {
  var context = $(this).closest('.row')[0];
  var template_row = $(".row-template", context);
  var row = template_row.clone();
  var element_total = $('.dynamic-table', context).find("tr").length;  // including template

  // Update name/id
  row.find(":input[id]").not(":button").each(function() {
    id = $(this).attr('id').replace(/-template-/, '-' + element_total + '-');
    $(this).attr('name', id).attr('id', id);
  });

  row.removeClass("row-template hidden");
  $('.dynamic-table', context).append(row);
  init_destination_select.call(row);
  init_select2.call(row);
  $(':input[type=password]', row).password();

  $('form').validator('update').validator('validate');

  template_row.trigger("row:cloned", row);

  $('.delete-row-entry', context).click(function(e) {
    e.preventDefault();
    $(this).closest("tr").remove();
    template_row.trigger("row:deleted", row);
    $('form').validator('update');
  });
}

function create_table_clientside() {
  var tables = $('table.client-side');
  var nbTables = tables.length;

  for (var i = 0; i < nbTables; i++) {
    var table = $(tables[i]).DataTable({ rowId: i});
    tableInstances.push(table);
    $(tables[i]).attr('data-row-id', i);

    function reloadActions(e, dt) {
      setTimeout(function() {
        init_events_on_datatable(tableInstances[dt.rowId]);
        build_column_actions(tableInstances[dt.rowId]);
      }, 300);
    }

    table.on('page.dt', reloadActions);
    table.on('search.dt', reloadActions);
    table.on('order.dt', reloadActions);

    init_datatable_buttons(table);
    init_events_on_datatable(table);
    build_column_actions(table);
  }
}

function init_events_on_datatable(datatable) {
  datatable.on('select.dt deselect.dt', function (e, dt) {
    if (!dt) {
      return;
    }

    var selected = dt.rows({selected: true}).count();
    if (selected > 0) {
      $('.delete-selected-rows').removeClass('disabled');
      $('.edit-selected-rows').removeClass('disabled');
    }
    else if (selected < 1) {
      $('.delete-selected-rows').addClass('disabled');
      $('.edit-selected-rows').addClass('disabled');
    }
    if (selected > 1) {
      $('.edit-selected-rows').addClass('disabled');
    }
  });

  var clicks = 0, delay = 400;
  datatable.on('mousedown','tbody tr td', function(event) {
    event.preventDefault();
    clicks++;

    setTimeout(function() {
      clicks = 0;
    }, delay);

    var is_editable = $(this).parent('tr').attr('data-editable') === 'True';
    var row_infos = get_row_infos($(this).parent('tr'));
    var is_column_actions = $(this).is('.data-column-actions');
    if (is_editable && ! is_column_actions && clicks === 2 && row_infos.get_url) {
      window.location.href = row_infos.get_url;
    }
  });
}


function init_destination_select() {
  $('.destination-select', this).on("select2:select", function() {
    toggle_destination.call(this);
  });
  $('.destination-select', this).each(function() {
    toggle_destination.call(this);
  });
}


function toggle_destination() {
  var context = $(this).closest('.destination-container');
  var destination = $('.destination-'+$(this).val(), context);

  var sub_dst_container = $('.destination-container div[class^=destination-]', context);
  $('[class^=destination-]', context).not('.destination-container').not(sub_dst_container).addClass('hidden');
  destination.removeClass("hidden");
  $('form').validator('update');
}


function init_select2() {
  $('.selectfield', this).each(function() {
    var select = $(this);
    if (select.parents('.row-template').length) {
      return;
    }
    var config = {
      theme: 'bootstrap',
      width: null,
    };

    var ajax_url = select.attr('data-listing_href') || select.attr('data-listing-href');
    var allow_custom_values = this.hasAttribute('data-allow_custom_values');
    if (allow_custom_values || ajax_url === ""){
      config['tags'] = true;
    }

    if (ajax_url) {
      config['placeholder'] = 'Select...';
      config['ajax'] = {
          url: ajax_url,
          delay: 450,
      };
      var ajax_data = select.attr('data-ajax_data');
      if (ajax_data) {
        config['ajax']['data'] = new Function("term", ajax_data);
      }

    } else {
      if (! config.tags) {
        config['minimumResultsForSearch'] = 5;
      }
    }

    var has_buttons_select_unselect_all = this.hasAttribute('data-select_unselect_all');
    if (has_buttons_select_unselect_all) {
      config['dropdownAdapter'] = $.fn.select2.amd.require('select2/selectAllAdapter')
    }

    var allow_clear = this.hasAttribute('data-allow_clear');
    if(select.attr('multiple') || allow_clear) {
      config['allowClear'] = true;
    }

    select.select2(config);

    var disable_sort = this.hasAttribute('data-disable_sort');
    if(select.attr('multiple') && ! disable_sort) {
      select2_sortable($(this));
    }

    fix_select2_placeholder_width_cutting_off_text();
  });
}

// https://github.com/select2/select2/issues/3817
function fix_select2_placeholder_width_cutting_off_text() {
  $('.select2-search__field').removeAttr('style');
}

// https://github.com/select2/select2/issues/3004
function select2_sortable($select2){
  var ul = $select2.next('.select2-container').find('ul.select2-selection__rendered');
  ul.sortable({
    placeholder : 'ui-state-highlight',
    forcePlaceholderSize: true,
    items       : 'li:not(.select2-search__field)',
    tolerance   : 'pointer',
    stop: function() {
      $($(ul).find('.select2-selection__choice').get().reverse()).each(function() {
        var id = $(this).data('data').id;
        var option = $select2.find('option[value="' + id + '"]')[0];
        $select2.prepend(option);
      });
    }
  });
}

function init_datatable_buttons(datatable) {
  var tableNode = datatable.table().node();
  var dataInfos = get_data_infos(tableNode);
  var tableName = $(tableNode).data('name') || 'view';
  var addForm = $('#' + tableName + '-add-form');

  datatable.button().add( 2, {
    className: 'btn edit-selected-rows disabled',
    text: '<i class="fa fa-edit"></i>',
    titleAttr: dataInfos.tooltips.get,
    action: function (e, dt, node, config) {
      dt.rows({selected: true}).every(function(rowIdx, tableLoop, rowLoop) {
        var row_infos = get_row_infos(this.nodes().to$());
        if (row_infos.get_url) {
          window.location.href = row_infos.get_url
        }
      });
    },
    init: function (dt, node) {
      node.attr('id', 'edit-selected-row');
    }
  });

  if (addForm.length || dataInfos.add_url) {
    datatable.button().add( 2, {
      className: 'btn',
      text: '<i class="fa fa-plus"></i>',
      titleAttr: dataInfos.tooltips.add,
      action: function () {
        var row_infos = get_row_infos($('thead tr', tableNode));
        if (row_infos.add_url) {
          window.location.href = addCurrentBreadcrumbs(row_infos.add_url);
        }
      },
      init: function (dt, node) {
        node.attr('id', 'add-form');
        node.attr('data-toggle', 'modal');
        node.attr('data-target', '#' + tableName + '-add-form');
        node.click(function () {
          $('form').validator('update');
        });
      }
    });
  }

  // CSV buttons
  var csvButtons = {
    'update': {icon: 'cloud-upload'},
    'export': {icon: 'download'},
    'import': {icon: 'upload'},
  };

  for(var action in csvButtons) {
    if (!dataInfos[action +'_url']) {
      continue;
    }
    var button = csvButtons[action];

    datatable.button().add(2, {
      className: 'btn',
      text: '<i class="fa fa-' + button.icon + '"></i> ' + action + ' CSV',
      titleAttr: dataInfos.tooltips[action],
      enabled: false,
      data: {
        actionName: action,
      },
      action: function () {
        // Export
        if (this.node()[0].attributes.title.value === 'Export') {
          window.location.href = dataInfos[this.node()[0].attributes.title.value.toLowerCase() +'_url'];
          return;
        }

        // Import & update
        $('#users-import-csv').modal('show')
      }
    });
  }
}


function get_delete_button(row_infos) {
  var delete_button = $('<a>', {
    href: row_infos.delete_url,
    class: 'btn btn-xs btn-default delete-entry',
    title: row_infos.tooltips.delete,
    onclick: "return confirm('Are you sure you want to delete this item?');"
  }).append($('<i>', {
    class: 'fa fa-times'
  }));

  return delete_button.prop('outerHTML');
}

function build_column_actions(datatable) {
  var $datatable = $(datatable.nodes().to$());

  $datatable.find('.delete-header').remove();
  $datatable.find('.data-column-actions').remove();
  $datatable.find('.delete-empty').remove();

  $datatable.find('thead tr').append("<th width='10' class='delete-header'></th>");
  $datatable.find('tbody tr').each(function() {
    var row_infos = get_row_infos($(this));
    if (row_infos.delete_url) {
      $(this).append('<td class="data-column-actions">' + get_delete_button(row_infos) + '</td>');
    } else {
      $(this).append('<td class="delete-empty"></td>');
    }
  });
}

// Used by wazo-ui-plugins
function create_table_serverside(config, actions_column=true, init_buttons=true, init_events=true) {
  let list_url = $('#table-list-serverside').attr('data-list_url');

  config.serverSide = true;
  config.processing = true;
  config.ajax = list_url;
  config.createdRow = function(row, data) {
    $(row).attr('data-uuid', data.uuid);
    $(row).attr('data-id', data.id);
    $(row).attr('data-tenant-uuid', data.tenant_uuid);
    $(row).attr('data-editable', 'True');
  };

  let Table = $('#table-list-serverside').DataTable(config);
  Table.on('xhr.dt', function() {
    setTimeout(function(){
        build_column_actions(Table);
    }, 300);
  });
  if (init_events) {
    init_events_on_datatable(Table);
  }
  if (init_buttons) {
    init_datatable_buttons(Table);
  }
  if (actions_column) {
    $(Table.nodes().to$()).find('thead tr').append("<th width='10'></th>");
  }
  // search only on 'enter', not on typing
  var input = $('#table-list-serverside_filter input');
  input.unbind();
  input.bind('keypress', function(e) {
    if (e.which == 13) {
      Table.search(this.value).draw();
    }
  });

  return Table;
}

function get_data_infos(table) {
  var tooltip = $('.table-data-tooltip', $(table));

  return {
    add_url: tooltip.attr('data-add_url'),
    get_url: tooltip.attr('data-get_url'),
    import_url: tooltip.attr('data-import_url'),
    export_url: tooltip.attr('data-export_url'),
    update_url: tooltip.attr('data-update_url'),
    delete_url: tooltip.attr('data-delete_url'),
    tooltips: {
      add: tooltip.attr('data-add_tooltip'),
      get: tooltip.attr('data-get_tooltip'),
      'delete': tooltip.attr('data-delete_tooltip'),
      'delete': tooltip.attr('data-delete_tooltip'),
      'import': tooltip.attr('data-import_tooltip'),
      'export': tooltip.attr('data-export_tooltip'),
      'update': tooltip.attr('data-update_tooltip'),
    }
  };
}

function addIdToURL(url, id) {
  const idx = url.indexOf('?');
  if (idx !== -1) {
    return url.substr(0, idx) + id + url.substr(idx, url.length);
  }

  return url + id;
}

function get_row_infos(row) {
  var data_uuid, data_id, data_tenant_uuid, data_non_unique_id;

  data_uuid = row.uuid ? row.uuid : row.attr('data-uuid');
  data_id = row.id ? row.id : row.attr('data-id');
  if (row.tenant_uuid) {
    data_tenant_uuid = row.tenant_uuid;
  } else {
    data_tenant_uuid = row.attr('data-tenant-uuid');
  }
  data_non_unique_id = row.attr('data-non-unique-id') === 'True';
  var data_infos = get_data_infos(row.parent().parent());

  if (data_tenant_uuid && data_non_unique_id) {
    if (data_infos.get_url) {
      data_infos.get_url = data_infos.get_url.slice(0, -1); // remove double /
      data_infos.get_url = addCurrentBreadcrumbs(data_infos.get_url + data_tenant_uuid + '/' + data_id);
    }
    if (data_infos.delete_url) {
      data_infos.delete_url = data_infos.delete_url.slice(0, -1); // remove double /
      data_infos.delete_url = data_infos.delete_url + data_tenant_uuid + '/' + data_id;
    }
  } else if (data_uuid || data_id) {
    data_infos.get_url = addCurrentBreadcrumbs(addIdToURL(data_infos.get_url, (data_uuid || data_id)));
    if (data_infos.delete_url) {
      data_infos.delete_url = addIdToURL(data_infos.delete_url, (data_uuid || data_id));
    }
  } else {
    delete data_infos.get_url;
    delete data_infos.delete_url;
  }

  return data_infos;
}

function addCurrentBreadcrumbs(link) {
  let hasParams = link.indexOf('?') !== -1;

  $('.breadcrumb li a').each(function(idx, crumb) {
    link += (!hasParams ? '?' : '&') + 'bc_names[]=' + crumb.innerText.trim();
    link += '&bc_urls[]=' + crumb.attributes.href.value.split('?')[0];
    link += '&bc_icons[]=' + ($('i', $(crumb)).attr('class') || '-').split('-')[1];

    hasParams = true;
  });

  return link;
}

function set_ajax_form(form, method="PUT") {
  form.find("#submit").attr("disabled", true);
  form.on("input change", function() {
    $(this).find("#submit").attr("disabled", false);
  });
  form.validator().submit(function(e) {
    if (!e.isDefaultPrevented()) {
      e.preventDefault();
      send_ajax_form(form, method);
    }
  });
}


function send_ajax_form(form, method) {
  $.ajax({
    type: method,
    url: $(form).attr('action'),
    data: $(form).serializeArray(),
    success: function(data, textStatus, jqXHR) {
      form_success(form, data, textStatus, jqXHR)
    }
  });
}


function form_success(form, results, textStatus, jqXHR) {
  var message = results.message;

  if (results.success) {
    // TODO not necessary to show success alert
    // update_alert('success', 'Success', message);
    // $("div.alert-success").fadeOut(3000);
    $(form).on("input change", function() {
      $(this).find("#submit").attr("disabled", false);
      $(this).find("#submit").attr("value", "Update");
      $(this).find("#submit").removeClass("btn-success").addClass("btn-primary");
    });
    $(form).find("#submit").attr("disabled", true);
    $(form).find("#submit").attr("value", "Saved");
    $(form).find("#submit").removeClass("btn-primary").addClass("btn-success");
  } else {
    var fill_form = results.fill_form;

    update_alert('error', 'Failed', message);
    for (var resource in fill_form) {
      if (!fill_form.hasOwnProperty(resource)) {
        continue;
      }
      for (var field_form in fill_form[resource]) {
        if (!fill_form[resource].hasOwnProperty(field_form)) {
          continue;
        }
        var message = fill_form[resource][field_form];

        $(form).find("#form-group-input-" + field_form + " > div.with-errors").html("<ul class='list-unstyled'><li>" + message + "</li></ul>");
        $(form).find("#form-group-input-" + field_form).parent(".form-group").addClass("has-error has-danger");
        $(form).find("#form-group-input-" + field_form).on("input change", function() {
          $(form).find("#form-group-input-" + field_form + " > div.with-errors").html("");
        })
      }
    }
  }
}


function update_alert(category, title, message) {
  var alert_box = $("div.alert-" + category);
  var alert_title = alert_box.find("#alert-title");
  var alert_message = alert_box.find("#alert-message");

  alert_box.toggleClass("hidden", false);
  alert_title.html(title);
  alert_message.html(message);
}
