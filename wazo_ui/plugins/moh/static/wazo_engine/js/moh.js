$(document).ready(function() {
  $('#mode').on('change', function (e) {
    toggle_moh_mode.call(this)
  })
  toggle_moh_mode.call($('#mode'))
});


function toggle_moh_mode() {
  if ($(this).val() == 'custom') {
    $('#application').closest('div.form-group').show()
    $('#sort').closest('div.form-group').hide()
  } else if ($(this).val() == 'files') {
    $('#sort').closest('div.form-group').show()
    $('#application').closest('div.form-group').hide()
  } else {
    $('#sort').closest('div.form-group').hide()
    $('#application').closest('div.form-group').hide()
  }
}