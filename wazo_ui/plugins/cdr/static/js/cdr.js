$(document).ready(function () {
  let table_config = {
    buttons: [
      'copy', 'csv', 'excel', 'pdf', 'print'
    ],
    columns: [
      {data: 'start'},
      {data: 'source_extension'},
      {data: 'source_name'},
      {data: 'destination_extension'},
      {data: 'destination_name'},
      {data: 'duration'},
      {data: 'answered'},
    ]
  };

  let Table = create_table_serverside(table_config, actions_column=false, init_buttons=false, init_events=false);
});
