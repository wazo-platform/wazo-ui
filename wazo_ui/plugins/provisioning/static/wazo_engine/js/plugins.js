$(document).ready(function() {
  let datatable_all_config = {
    buttons: []
  };
  let datatable_all = $('#table-list-all').DataTable(datatable_all_config);
  datatable_all.buttons($('.buttons-select-all')).remove();
  datatable_all.buttons('.buttons-select-none').remove();
  datatable_all.buttons('.edit-selected-rows').remove();

  let datatable_unalloc = $('#table-list-unallocated').DataTable(datatable_all_config);
  datatable_unalloc.buttons('.edit-selected-rows').remove();
  datatable_unalloc.buttons('.edit').remove();

  $('.link-install-plugin').mouseover(function () {
    $(this).attr('title', $(this).data('original-title'));
  });
  $('.link-uninstall-plugin').mouseover(function () {
    $(this).attr('title', $(this).data('original-title'));
  });

  $('.link-install-plugin, .link-uninstall-plugin').on('shown.bs.confirmation', function(){
    var $parentLink = $(this);
    var pollURL = $parentLink.attr('data-poll-url');

    function displayError(error) {
      $('.modal-title').html('Error');
      $('.modal-body').html(error).addClass('text-danger');
    }

    function pollCommandStatus(commandLocation) {
      $.ajax(pollURL + '?location=' + commandLocation).done(function(data){
        if(data.state === 'success') {
          location.reload();
          return;
        }

        if(data.state === 'fail') {
          return displayError('An error occurred while installing the package.');
        }

        setTimeout(function() {
          pollCommandStatus(commandLocation);
        }, 3000);
      }).fail(displayError);
    }

    $('.confirmation-buttons a').on('click', function(e) {
      $('.modal-body').html('Processing your plugin, please wait ...').removeClass('text-danger');
      $('.modal-title').html('Processing');
      $('#download-status-modal').modal('show');

      // When installing a package, wait for process to finish
      if ($parentLink.hasClass('ajax')) {
        e.preventDefault();

        $.ajax($parentLink.attr('href')).done(function(data){
          if(data.state === 'progress') {
            return setTimeout(function() {
              pollCommandStatus(data.location);
            }, 3000);
          }

          location.reload();
        }).fail(displayError);

        return false;
      }
    });
  });
});
