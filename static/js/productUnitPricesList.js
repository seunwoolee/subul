 function fetch_data(start_date='', end_date='')
 {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let location = $('.type_filter #location select').val();
    let product = $('.type_filter #product select').val();

    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "responsive": true,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: -1, orderable: false },
        ],
        "language": {searchPlaceholder: "거래처명, 제품명, 메모"},
        "processing": true,
        "serverSide": true,
        "order" : [[0, "asc"]],
        "ajax": {
            "url": "/api/productUnitPrices/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date, location:location, product:product
            }
        },
        "columns": [
            {"data": "id"},
            {"data": "locationCode"},
            {"data": "locationCodeName"},
            {"data": "productCode"},
            {"data": "productCodeName"},
            {"data": "price", "render": $.fn.dataTable.render.number( ',')},
            {"data": "specialPrice", "render": $.fn.dataTable.render.number( ',')},
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
    $('#modifyModal .price').val(data['price']);
    $('#modifyModal .specialPrice').val(data['specialPrice']);
    $('#modifyModal .codeName').text(data['locationCodeName'] + '('+data['productCodeName']+')');
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
    let $this = $(this);
    let data = $this.serialize();
    let type = $this.find('.ajaxUrlType').val();
    let url = '/api/productUnitPrices/'+id;

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

$(document).on('click', "#create", function()
{
    let location = $('.type_filter #location select').val();
    let product = $('.type_filter #product select').val();
    let locationCodeName = $('.type_filter #location select option:selected').text();
    let productCodeName = $('.type_filter #product select option:selected').text();

    if (location && product)
    {
        $('#createModal #id_locationCode').val(location);
        $('#createModal #id_productCode').val(product);
        $('#createModal .codeName').text(locationCodeName + '('+productCodeName+')');
        $("#createModal").modal();
    }
    else
    {
        alert("장소와 제품을 모두 선택 해주세요");
    }
});

$('.create').on('submit', function (e)
{
    e.preventDefault();

    let $this = $(this);
    let data = $this.serialize();
    let type = $this.find('.ajaxUrlType').val();
    let url = '/api/productUnitPrices/';

    $.ajax({
    url: url,
    type: type,
    data: data,
    }).done(function(data) {
        alert('완료');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('이미 존재하는 거래처별 제품입니다. 수정이나 삭제를 해주세요');
    });
});
