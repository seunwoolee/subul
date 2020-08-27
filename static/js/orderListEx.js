fetch_data(end_day, plusThree_day);
$('#start_date').val(end_day);
$('#end_date').val(plusThree_day);

function fetch_data(start_date = '', end_date = '') {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);

    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "responsive": true,
        "searching": false,
        "language": {searchPlaceholder: "품명"},
        "processing": true,
        "serverSide": true,
        "order": [[0, "asc"]],
        "ajax": {
            "url": "/api/orderEx/?format=datatables",
            "type": "GET",
            "data": { start_date: start_date, end_date: end_date }
        },
        "columns": [
            {"data": "id"},
            {
                "data": "ymd", "render": function (data, type, row, meta) {
                    return set_yyyy_mm_dd(data);
                }
            },
            {
                "data": "weekday", "render": function (data, type, row, meta) {
                    return setWeekdayButton(data);
                }
            },
            {"data": "orderLocationName"},
            {"data": "codeName"},
            {"data": "amount", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "count", "render": $.fn.dataTable.render.number(',')},
            {"data": "price", "render": $.fn.dataTable.render.number(',', '.', 1)},
            {"data": "totalPrice", "render": $.fn.dataTable.render.number(',')},
            {"data": "memo"},
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

function setWeekdayButton(data) {
    switch (data) {
        case '월':
            return '<span class="badge badge-pill badge-primary">' + data + '</span>'
            break;
        case '화':
            return '<span class="badge badge-pill badge-secondary">' + data + '</span>'
            break;
        case '수':
            return '<span class="badge badge-pill badge-success">' + data + '</span>'
            break;
        case '목':
            return '<span class="badge badge-pill badge-danger">' + data + '</span>'
            break;
        case '금':
            return '<span class="badge badge-pill badge-warning">' + data + '</span>'
            break;
        case '토':
            return '<span class="badge badge-pill badge-info">' + data + '</span>'
            break;
        case '일':
            return '<span class="badge badge-pill badge-dark">' + data + '</span>'
            break;
        default :
            return '오류'
    }
}
