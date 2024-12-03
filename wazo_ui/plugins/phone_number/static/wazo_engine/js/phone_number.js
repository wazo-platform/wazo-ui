function selectMainPhoneNumber(uuid) {
    let button = $('#main_phone_number-'+uuid);
    let url = button.context.URL+'/select_main_number';
    let body = {number_uuid: uuid};
    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(body),
        success: function(data) {
            location.reload();
            console.log('success');
        },
        error: function(data) {
            console.log('error');
            setTimeout(function() {
                console.log('There is some error, please reload');
                location.reload();
            }, 4000);
        }
    });
}
