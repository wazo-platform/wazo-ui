$(document).ready(function() {
  var checkbox = $('input[type="checkbox"].verify_certificate');

  function disableField() {
    if(checkbox.is(':checked')){
      $('input.certificate_path').removeAttr('disabled');
    } else {
      $('input.certificate_path').attr('disabled', 'disabled');
    }
  }

  checkbox.click(disableField);
  disableField();
});

$(document).ready(function() {
    var verify_certificate = $('input[type="checkbox"].auth_verify_certificate');
    var https = $('input[type="checkbox"].auth_https');

    function disablePathField() {
        if(verify_certificate.is(':checked')){
            $('input.auth_certificate_path').removeAttr('disabled');
        } else {
            $('input.auth_certificate_path').attr('disabled', 'disabled');
        }
    }

    function disableCertificateField() {
        if(https.is(':checked')){
            $('input.auth_verify_certificate').removeAttr('disabled');
            $('input.auth_certificate_path').removeAttr('disabled');
        } else {
            $('input.auth_verify_certificate').attr('disabled', 'disabled');
            $('input.auth_certificate_path').attr('disabled', 'disabled');
        }
    }

    verify_certificate.click(disablePathField);
    https.click(disableCertificateField);
    disableCertificateField();
    disablePathField();
});

$(document).ready(function() {
    var checkbox = $('input[type="checkbox"].confd_verify_certificate');

    function disableField() {
        if(checkbox.is(':checked')){
            $('input.confd_certificate_path').removeAttr('disabled');
        } else {
            $('input.confd_certificate_path').attr('disabled', 'disabled');
        }
    }

    checkbox.click(disableField);
    disableField();
});
