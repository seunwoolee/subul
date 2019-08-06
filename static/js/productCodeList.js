fetch_data();

function fetch_data(start_date = '', end_date = '') {
    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "responsive": true,
        "language": {searchPlaceholder: "제품명"},
        "processing": true,
        "serverSide": true,
        "order": [[0, "asc"]],
        "ajax": {
            "url": "/api/productCode/?format=datatables",
            "type": "GET",
        },
        "columns": [
            {"data": "id", searchable: false},
            {"data": "code", searchable: false},
            {"data": "codeName"},
            {"data": "type", searchable: false},
            {"data": "amount_kg", searchable: false},
            {"data": "calculation", searchable: false},
            {"data": "expiration"},
            {
                "data": null, "render": function (data, type, row, meta) {
                    return setDataTableActionButtonOnlyModify();
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
    $('#id_calculation').val(data['calculation']);
    $('#id_expiration').val(data['expiration']);
    $('.codeName').text(data['codeName']);
    $("#modifyModal").modal();
}

$('#modifyModal form').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let data = $this.serialize();
    let url = '/api/productCode/' + id;
    debugger;

    $.ajax({
        url: url,
        type: 'patch',
        data: data,
    }).done(function (data) {
        alert('완료');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function () {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});
