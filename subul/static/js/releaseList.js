
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
            {"data": "specialTag", "render" : function(data, type, row, meta){return setSpecialTagButton(data);}},
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
            {"data": null, "render": function(data, type, row, meta){return setDataTableActionButton();}}
        ],
        dom: 'Bfrtip',
        buttons: ['pageLength', 'colvis','copy', 'excel', 'pdf', 'print'],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
 }

//
//$('.datatable tbody').on('click', 'button', function () {
//    let data = table.row($(this).parents('tr')).data();
//    let class_name = $(this).attr('class');
//    if (class_name == 'btn btn-info btn-sm MODIFY')  // EDIT button
//    {
//        if(data['type'] == "제품생산")
//        {
//            $('#amount').val(data['amount']);
//            $('#count').val(data['count']);
//            $('.memo').val(data['memo']);
//            $('.modal_title').text('EDIT');
//            $('.codeName').text(data['codeName']);
//            $('.productType').val('product');
//            $("#productModal").modal();
//        }
//        else // 할란, 할란사용, 공정품투입, 공정품발생
//        {
//            if(data['codeName'].indexOf('RAW') != -1)
//            {
//                tank_amount = data['rawTank_amount'];
//                $('#tank_amount').val(tank_amount).attr("name","rawTank_amount");
//            }
//            else
//            {
//                tank_amount = data['pastTank_amount'];
//                $('#tank_amount').val(tank_amount).attr("name","pastTank_amount");
//            }
//            $('.productType').val('productEgg');
//            $('.memo').val(data['memo']);
//            $('.type').val('edit');
//            $('.modal_title').text('EDIT');
//            $('.codeName').text(data['codeName']);
//            $("#productEggModal").modal();
//        }
//    }
//    else if(class_name == 'btn btn-danger btn-sm REMOVE')// DELETE button
//    {
//        if(data['type'] == "제품생산")
//        {
//            $('.productType').val('product');
//        }
//        else
//        {
//            $('.productType').val('productEgg');
//        }
//        $('#modal_title').text('DELETE');
//        $("#confirm").modal();
//    }
//
//    id = data['id'];
//
//});


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