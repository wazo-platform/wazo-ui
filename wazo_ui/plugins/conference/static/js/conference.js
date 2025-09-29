$(document).ready(function () {
  $('.conference-context').on("change", function (e) {
    add_available_extensions();
  });
  add_available_extensions();
});

function add_available_extensions() {
  let extension_select = $(".conference-exten");
  let context_select = $(".conference-context");
  let ajax_url = $(extension_select).attr('data-listing-href');
  if (!ajax_url) {
    return;
  }

  if (!extension_select.val()) {
    extension_select.append("<option></option>")
  }

  extension_select.select2({
    allowClear: true,
    placeholder: 'Select...',
    theme: 'bootstrap',
    tags: true,
    ajax: {
      url: ajax_url,
      data: function (params) {
        return {
          term: params.term,
          context: context_select.val()
        }
      }
    },
  });
}
