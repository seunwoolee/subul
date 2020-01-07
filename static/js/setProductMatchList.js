 function fetch_data(start_date='', end_date='')
 {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let location = $('.type_filter #location select').val();
    let setProduct = $('.type_filter #setProduct select').val();

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
            "url": "/api/setProductMatch/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date, location:location, setProduct:setProduct
            }
        },
        "columns": [
            {"data": "id"},
            {"data": "saleLocation"},
            {"data": "saleLocationCodeName"},
            {"data": "setProductCode"},
            {"data": "setProductCodeName"},
            {"data": "productCode"},
            {"data": "productCodeName"},
            {"data": "price", "render": $.fn.dataTable.render.number(',', '.', 1)},
            {"data": "count", "render": $.fn.dataTable.render.number( ',')},
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
    $('#modifyModal .count').val(data['count']);
    $('#modifyModal .codeName').text(data['productCodeName'] + '('+data['setProductCodeName']+')');
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
    let url = '/api/setProductMatch/'+id;

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
    let setProduct = $('.type_filter #setProduct select').val();
    let setProductCodeName = $('.type_filter #setProduct select option:selected').text();

    if (location && setProduct)
    {
        $('#createModal #id_locationCode').val(location);
        $('#createModal #id_setProductCode').val(setProduct);
        $('#createModal .codeName').text(setProductCodeName);
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
    let url = '/api/setProductMatch/';

    $.ajax({
    url: url,
    type: type,
    data: data,
    }).done(function(data) {
        alert('완료');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('이미 존재하는 제품입니다. 수정이나 삭제를 해주세요.');
    });
});
