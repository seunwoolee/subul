fetch_data();

function fetch_data() {
    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "responsive": true,
        "language": {searchPlaceholder: "회사명"},
        "processing": true,
        "serverSide": true,
        "order": [[0, "asc"]],
        "ajax": {
            "url": "/api/orderTime/?format=datatables",
            "type": "GET"
        },
        "columns": [
            {"data": "id", "searchable": false},
            {"data": "company_name", "searchable": true},
            {"data": "weekday", "searchable": false},
            {"data": "start", "searchable": false},
            {"data": "end", "searchable": false},
            {
                "data": null, "render": function (data, type, row, meta) {
                    // return setDataTableActionButton();
                    return setDataTableActionButtonOnlyDelete();
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

function deleteButtonClick(data) {
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

$('.deleteAndEdit').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let data = $this.serialize();
    let type = $this.find('.ajaxUrlType').val();
    let url = '/api/orderTime/' + id;

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

function editButtonClick(data) {
    $('#modifyModal #id_car_number').val(data['car_number']);
    $('#modifyModal #id_type').val(data['type']);
    $('#modifyModal #id_pallet_count').val(data['pallet_count']);
    $("#modifyModal").modal();
}
