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
var table;
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
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date
            }
        },
        "columns": [
            {'data': 'id'},
            {'data': 'ymd'},
            {'data': 'releaseLocationName'},
            {'data': 'contentType'},
            {'data': 'code'},
            {'data': 'codeName'},
            {'data': 'amount'},
            {'data': 'count'},
            {'data': 'kgPrice'},
            {'data': 'totalPrice'},
            {'data': 'supplyPrice'},
            {'data': 'releaseVat'},
            {"data": "eaPrice"},
            {"data": "productYmd"},
            {"data": "type"},
            {"data": "releaseStoreLocationCodeName"},
            {"data": "orderMemo"},
            {"data": "locationType"},
            {"data": "locationManagerName"},
            {'data': 'releaseSetProduct', "visible": false},
            {'data': 'releaseSetProductCodeName', "visible": false},
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


// function fetch_data(start_date='', end_date='')
// {
//    table = $('.datatable').DataTable({
//        "processing": true,
//        "serverSide": true,
//        "ajax": {
//            "url": "/api/release/",
//            "type": "GET",
//            "data": {
//                start_date:start_date, end_date:end_date
//            }
//        },
//        "columns": [
//            {'data': 'id'},
//            {'data': 'ymd'},
//            {'data': 'releaseLocationName'},
//            {'data': 'contentType'},
//            {'data': 'code'},
//            {'data': 'codeName'},
//            {'data': 'amount'},
//            {'data': 'count'},
//            {'data': 'kgPrice'},
//            {'data': 'totalPrice'},
//            {'data': 'supplyPrice'},
//            {'data': 'releaseVat'},
//            {'data': 'eaPrice'},
//            {'data': 'productYmd'},
//            {'data': 'type'},
//            {'data': 'releaseStoreLocation'},
//            {'data': 'orderMemo'},
//            {'data': 'locationType'},
//            {'data': 'locationManager'},
//            {'data': 'releaseSetProductCode'},
//            {'data': 'releaseSetProductCodeName'},
//            {
//                "data": null,
//                "defaultContent": '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="fa fa-trash-o"></i></button>' +
//                                    '<button class="btn btn-info btn-sm MODIFY" href="#"><i class="fa fa-edit"></i></button>'
//            }
//        ],
//        dom: 'Bfrtip',
//        buttons: ['pageLength', 'colvis', 'copy', 'excel', 'pdf', 'print'],
//        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
//    });
// }

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
        if(data['type'] == "제품생산")
        {
            $('#amount').val(data['amount']);
            $('#count').val(data['count']);
            $('.memo').val(data['memo']);
            $('.modal_title').text('EDIT');
            $('.codeName').text(data['codeName']);
            $('.productType').val('product');
            $("#productModal").modal();
        }
        else // 할란, 할란사용, 공정품투입, 공정품발생
        {
            if(data['codeName'].indexOf('RAW') != -1)
            {
                tank_amount = data['rawTank_amount'];
                $('#tank_amount').val(tank_amount).attr("name","rawTank_amount");
            }
            else
            {
                tank_amount = data['pastTank_amount'];
                $('#tank_amount').val(tank_amount).attr("name","pastTank_amount");
            }
            $('.productType').val('productEgg');
            $('.memo').val(data['memo']);
            $('.type').val('edit');
            $('.modal_title').text('EDIT');
            $('.codeName').text(data['codeName']);
            $("#productEggModal").modal();
        }
    }
    else if(class_name == 'btn btn-danger btn-sm REMOVE')// DELETE button
    {
        if(data['type'] == "제품생산")
        {
            $('.productType').val('product');
        }
        else
        {
            $('.productType').val('productEgg');
        }
        $('#modal_title').text('DELETE');
        $("#confirm").modal();
    }

    id = data['id'];

});


$('form').on('submit', function (e)  // EDIT
{
    e.preventDefault();
    $this = $(this);
    let data = $this.serialize();
    url = makeAjaxUrl($this);

    $.ajax({
    url: url,
    type: 'patch',
    data: data,
    }).done(function(data) {
        alert('수정완료');
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

function makeAjaxUrl($this)
{
    let productType = $this.find("input[name='productType']").val();
    if(productType == 'product')
    {
        url = '/api/product/'+id;
    }
    else if(productType == 'productEgg')
    {
        url = '/api/productEgg/'+id;
    }
    return url;
}
