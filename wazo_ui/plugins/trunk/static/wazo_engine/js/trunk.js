$(document).ready(function () {
  $('#endpoint_sip-host').on('change', function (e) {
    toggle_endpoint_sip_host_mode.call(this)
  })
  toggle_endpoint_sip_host_mode.call($('#endpoint_sip-host'))
  $('#endpoint_iax-host').on('change', function (e) {
    toggle_endpoint_iax_host_mode.call(this)
  })
  toggle_endpoint_iax_host_mode.call($('#endpoint_iax-host'))
  $('#register_sip-enabled').on('change', function (e) {
    toggle_register_form('sip');
  });
  toggle_register_form('sip');
  $('#register_iax-enabled').on('change', function (e) {
    toggle_register_form('iax');
  });
  toggle_register_form('iax');
  $("[id$='auth_username']").on('change', function (e) {
    toggle_register_auth_validator();
  });
  $('#register_iax-callback_context').on('change', function (e) {
    toggle_register_iax_callback_validator();
  });
});


function toggle_register_auth_validator() {
    if ($("[id$='auth_username']").val().length > 0) {
      $("[id$='auth_password']").attr('required', 'required');
    } else {
      $("[id$='auth_password']").removeAttr('required');
    }
    $('form').validator('update');
}


function toggle_register_iax_callback_validator() {
    if ($('#register_iax-callback_context').val().length > 0) {
      $('#register_iax-callback_extension').attr('required', 'required');
    } else {
      $('#register_iax-callback_extension').removeAttr('required');
    }
    $('form').validator('update');
}


function toggle_endpoint_sip_host_mode() {
  if ($(this).val() == 'dynamic') {
    $('#endpoint_sip-host_value').closest('div.form-group').hide()
  } else {
    $('#endpoint_sip-host_value').closest('div.form-group').show()
  }
}


function toggle_endpoint_iax_host_mode() {
  if ($(this).val() == 'dynamic') {
    $('#endpoint_iax-host_value').closest('div.form-group').hide()
  } else {
    $('#endpoint_iax-host_value').closest('div.form-group').show()
  }
}


function toggle_register_form(protocol) {
  if ($('input[name="register_' + protocol + '-enabled"]:checked').length > 0) {
    $('[id^=register_' + protocol + '-]:input:not(#register_' + protocol + '-enabled)').closest('div.form-group').show()
    $('[id^=register_' + protocol + '-][required]').each(function () {
      $(this).attr('data-validate', true)
    });
  } else {
    $('[id^=register_' + protocol + '-]:input:not(#register_' + protocol + '-enabled)').closest('div.form-group').hide()
    $('[id^=register_' + protocol + '-][required]').each(function () {
      $(this).attr('data-validate', false)
    });
  }
  $('form').validator('update');
}
