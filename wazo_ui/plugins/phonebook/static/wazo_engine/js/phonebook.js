$('#phonebook').on('change', (ev) => {
    var queryParams = new URLSearchParams(window.location.search);
    queryParams.set("phonebook_uuid", ev.target.value);
    history.replaceState(null, null, "?" + queryParams.toString());
    window.location.href = "?" + queryParams.toString();
})
