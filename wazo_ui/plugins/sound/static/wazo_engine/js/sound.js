$(document).ready(function() {
  let table_config = {
    buttons: []
  };

  $('#table-list-sound-files-system').DataTable(table_config);
  let datatable_list_sound_files = $('#table-list-sound-files').DataTable(table_config);

  datatable_list_sound_files.button().add( 0, {
    className: 'btn',
    text: '<i class="fa fa-plus"></i>',
    init: function (dt, node, config) {
      node.attr('id', 'add-form');
      node.attr('data-toggle', 'modal');
      node.attr('data-target', '#view-add-form');
      node.click(function () {
        $('#view-add-form').removeClass('hidden').removeAttr('style');
        $('form').validator('update');
      });
    }
  });
});
