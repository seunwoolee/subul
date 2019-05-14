function fetch_data() {
    let packing = $('.type_filter #packing select').val();
    let product = $('.type_filter #product select').val();

    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "responsive": true,
        "columnDefs": [
            {responsivePriority: 1, targets: 0},
            {responsivePriority: 2, targets: -1, orderable: false},
        ],
        "processing": true,
        "serverSide": true,
        "searching": false,
        "order": [[0, "asc"]],
        "ajax": {
            "url": "/api/autoPacking/",
            "type": "GET",
            "data": {packing: packing, product: product}
        },
        "columns": [
            {"data": "id"},
            {"data": "packingCodeName"},
            {"data": "productCodeName"},
            {"data": "count", "render": $.fn.dataTable.render.number(',')},
            {
                "data": null, "render": function (data, type, row, meta) {
                    return setDataTableActionButton();
                }
            }
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excel',
                className: 'btn btn-light',
                text: '<i class="far fa-file-excel fa-lg"></i>',
                init: function (api, node, config) {
                    $(node).removeClass('btn-secondary');
                }
            }],
        lengthMenu: [[30, 50, -1], [30, 50, "All"]],
    });
}

function editButtonClick(data) {
    $('#modifyModal #modify_id_packingCode').val(data['packingCode']);
    $('#modifyModal #modify_id_productCode').val(data['productCode']);
    $('#modifyModal #modify_id_count').val(data['count']);
    $('#modifyModal .codeName').text(data['packingCodeName'] + '(' + data['productCodeName'] + ')');
    $("#modifyModal").modal();
}

function deleteButtonClick(data) {
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

$('.deleteAndEdit').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let data = $this.serialize();
    let type = $this.find('.ajaxUrlType').val();
    let url = '/api/autoPacking/' + id;

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('완료');
        $('.datatable').DataTable().draw();
        $(".everyModal").modal('hide');
    }).fail(function () {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

$(document).on('click', "#create", function () {
    let packing = $('.type_filter #packing select').val();
    let product = $('.type_filter #product select').val();
    let packingCodeName = $('.type_filter #packing select option:selected').text();
    let productCodeName = $('.type_filter #product select option:selected').text();

    if (packing && product) {
        $('#createModal #id_packingCode').val(packing);
        $('#createModal #id_productCode').val(product);
        $('#createModal .codeName').text(packingCodeName + '(' + productCodeName + ')');
        $("#createModal").modal();
    } else {
        alert("포장재와 제품을 모두 선택 해주세요");
    }
});

$('.create').on('submit', function (e) {
    e.preventDefault();

    let $this = $(this);
    let data = $this.serialize();
    let type = 'post';
    let url = '/api/autoPacking/';

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('완료');
        $('.datatable').DataTable().draw();
        $(".everyModal").modal('hide');
    }).fail(function () {
        alert('에러발생');
    });
});
