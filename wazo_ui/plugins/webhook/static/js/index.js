$('#services').on('change', function() {
  var service = $(this).val();
  hide_services();
  if (service) {
    $('#' + service).removeClass('hidden');
  }
})

function hide_services() {
  $('#services option').each(function() {
    var service = $(this).val();
    $('#' + service).addClass('hidden');
  })
}
