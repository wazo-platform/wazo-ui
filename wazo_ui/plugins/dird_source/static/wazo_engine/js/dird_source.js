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
    var checkbox = $('input[type="checkbox"].auth_verify_certificate');

    function disableField() {
        if(checkbox.is(':checked')){
            $('input.auth_certificate_path').removeAttr('disabled');
        } else {
            $('input.auth_certificate_path').attr('disabled', 'disabled');
        }
    }

    checkbox.click(disableField);
    disableField();
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
