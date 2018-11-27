$('#search').click(function(){
  var start_date = $('#start_date').val();
  var end_date = $('#end_date').val();
  if(start_date != '' && end_date !='')
  {
       $('.datatable').DataTable().destroy();
       fetch_data(start_date, end_date);
  }
  else
  {
       alert("날짜를 모두 입력해주세요");
  }
 });

 $('.datatable tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info btn-sm MODIFY')
    {
        editButtonClick(data);
    }
    else if(class_name == 'btn btn-danger btn-sm REMOVE')
    {
        deleteButtonClick(data);
    }
        id = data['id'];
});