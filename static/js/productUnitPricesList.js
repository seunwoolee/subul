 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
 fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let location = $('.type_filter #location select').val();

    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "responsive": true,
        "paging": false,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: -1, orderable: false },
        ],
        "language": {searchPlaceholder: "거래처명, 제품명, 메모",info: ""},
        "processing": true,
        "serverSide": true,
        "order" : [[5, "asc"]],
        "ajax": {
            "url": "/api/productUnitPrices/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date, location:location
            }
        },
        "columns": [
            {"data": "id"},
            {"data": "locationCode"},
            {"data": "locationCodeName"},
            {"data": "productCode"},
            {"data": "productCodeName"},
            {"data": "price"},
            {"data": "specialPrice"},
            {"data": null, "render": function(data, type, row, meta){return setDataTableActionButton();}}
        ],
        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]],
    });


 }

function editButtonClick(data)
{
    $('#modify_id_purchaseSupplyPrice').val(data['purchaseSupplyPrice']);
    $('#modify_id_purchaseVat').val(data['purchaseVat']);
    $('#modify_id_memo').val(data['memo']);
    $('.codeName').text(data['codeName']);
    $("#modifyModal").modal();
}

function deleteButtonClick(data)
{
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

$('.deleteAndEdit').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();
    let url = '/api/productOEM/'+id;

    $.ajax({
    url: url,
    type: type,
    data: data,
    }).done(function(data) {
        alert('완료');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

//$('form').on('submit', function (e)
//{
//    e.preventDefault();
//    $this = $(this);
//    let data = $this.serialize();
//    let type = $this.find('.ajaxUrlType').val();
//    url = setAjaxUrl($this);
//
//    $.ajax({
//    url: url,
//    type: type,
//    data: data,
//    }).done(function(data) {
//        alert('완료');
//        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
//        $(".everyModal").modal('hide');
//    }).fail(function() {
//        alert('수정 에러 전산실로 문의바랍니다.');
//    });
//});