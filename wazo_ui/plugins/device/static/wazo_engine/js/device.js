$(document).ready(function() {
  let datatable = $('#table-list').DataTable();

  datatable.button().add( 5, {
    className: 'btn sync-selected-rows',
    text: '<i class="fa fa-arrows-h"></i>',
    titleAttr: 'Synchronize selected devices',
    action: function (e, dt, node, config) {
      if (confirm('Are you sure you want to synchronize these devices ?')) {
        dt.rows({selected: true}).every(function(rowIdx, tableLoop, rowLoop) {
          let row = this.nodes().to$();
          $.ajax({
            url: row.find('#link-synchronize-device').attr('href'),
            type: 'GET'
          });
          row.removeClass('selected');
        });
      }
    }
  });
  $('#link-synchronize-device').mouseover(function () {
    $(this).attr('title', $(this).data('original-title'));
  });
  $('#link-reset-device').mouseover(function () {
    $(this).attr('title', $(this).data('original-title'));
  });
});
