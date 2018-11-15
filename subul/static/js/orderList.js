/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.1.1): datatables.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------

 */


var date = new Date();
var days = 7;
var plusSevenDate = new Date(date.getTime() + (days * 24 * 60 * 60 * 1000));
var start_day = date.yyyymmdd();
var end_day = plusSevenDate.yyyymmdd();

 $('.input-daterange').datepicker({
  todayBtn:'linked',
  format: "yyyymmdd",
  autoclose: true
 });


 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
    table = $('.datatable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date
            }
        },
        "columns": [
            {"data": "id"},
            {
                "data": "type",
                "render" : function(data, type, row, meta){
                    if(data == '판매')
                    {
                        return '<button class="btn btn-danger btn-sm">'+ data +'</button>'
                    }
                    else if(data == '샘플')
                    {
                        return '<button class="btn btn-warning btn-sm">'+ data +'</button>'
                    }
                    else if(data == '증정')
                    {
                        return '<button class="btn btn-success btn-sm">'+ data +'</button>'
                    }
                    else if(data == '자손')
                    {
                        return '<button class="btn btn-primary btn-sm ">'+ data +'</button>'
                    }
                    else if(data == '생산요청')
                    {
                        return '<button class="btn btn-dark btn-sm">'+ data +'</button>'
                    }
                }
            },
            {"data": "ymd"},
            {"data": "orderLocationName"},
            {"data": "codeName"},
            {"data": "amount"},
            {"data": "count"},
            {"data": "price"},
            {"data": "totalPrice"},
            {"data": "memo"},
            {"data": "setProduct"},
            {
                "data": null,
                "defaultContent": '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="fa fa-trash-o"></i></button>' +
                                    '<button class="btn btn-info btn-sm MODIFY" href="#"><i class="fa fa-edit"></i></button>'
            }
        ],
        dom: 'Bfrtip',
        buttons: ['pageLength', 'colvis','copy', 'excel', 'pdf', 'print'],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
 }

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
    if (class_name == 'btn btn-info btn-sm MODIFY')  // EDIT button
    {
        $('#amount').val(data['amount']);
        $('#count').val(data['count']);
        $('#price').val(data['price']);
        $('.memo').val(data['memo']);
        $('.modal_title').text('EDIT');
        $('.codeName').text(data['codeName']);
        $("#orderModal").modal();
    }
    else if(class_name == 'btn btn-danger btn-sm REMOVE')// DELETE button
    {
        $('#modal_title').text('DELETE');
        $("#confirm").modal();
    }

    id = data['id'];

});


$('form').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let data = $this.serialize();
    url = '/api/order/'+id;

    $.ajax({
    url: url,
    type: 'patch',
    data: data,
    }).done(function(data) {
        console.log(data);
        alert('수정완료');
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});


