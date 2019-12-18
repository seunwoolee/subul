$('#start_date').val(end_day);
$('#end_date').val(plusSeven_day);
$('#id_ymd').val(set_yyyymmdd(end_day));
fetch_data(end_day, plusSeven_day);
function fetch_data(start_date = '', end_date = '') {

    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);

    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "responsive": true,
        "columnDefs": [
            {responsivePriority: 1, targets: 0},
            {responsivePriority: 2, targets: -1, orderable: false},
        ],
        "language": {searchPlaceholder: "제품명, 메모"},
        "processing": true,
        "serverSide": true,
        "order": [[0, "asc"]],
        "ajax": {
            "url": "/api/productOrder/",
            "type": "GET",
            "data": {'start_date': start_date, 'end_date': end_date}
        },
        "select": true,
        "columns": [
            {"data": "id"},
            {"data": "ymd"},
            {
                "data": "type", "render": function (data, type, row, meta) {
                    return productOrderTypeButton(data);
                }
            },
            {
                "data": "display_state", "render": function (data, type, row, meta) {
                    return orderDisplayButton(data);
                }
            },
            {"data": "code"},
            {"data": "codeName"},
            {"data": "real_count"},
            {"data": "real_amount"},
            {"data": "memo"},
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
        rowCallback: function (row, data, index) {
            $('td:eq(1)', row).html(set_yyyy_mm_dd(data.ymd));
        }
    });
}

function productOrderTypeButton(data) {
    switch (data) {
        case '전란':
            return '<button class="btn btn-warning btn-sm">' + data + '</button>';
        case '난백난황':
            return '<button class="btn btn-primary btn-sm">' + data + '</button>';
    }
}

$('#create').click(function () {
    let start_date = set_yyyymmdd($('#start_date').val());
    let end_date = set_yyyymmdd($('#end_date').val());
    let content_type = '난백난황';

    if (confirm(`${start_date} 생산지시를 하시겠습니까?`)) {

        if (confirm(`전란 생산을 지시하시겠습니까`)) {
            content_type = '전란'
        }

        $.ajax({
            url: 'product/order',
            type: 'post',
            data: {'start_date': start_date, 'end_date': end_date, 'content_type': content_type},
        }).done(function (data) {
            alert('완료');
        }).fail(function (e) {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    }
});

function deleteButtonClick(data) {
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

$('.delete').on('submit', function (e) {
    e.preventDefault();
    let type = 'delete';
    let data = $(this).serialize();
    let url = '/api/productOrder/' + id;

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('수정완료');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function () {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

$('.open-button').click(function () {
    $('#createForm').css('display', 'block');
});

$('.close-button').click(function () {
    $('#createForm').css('display', 'none');
});

$('#finish').click(function () {
    let start_date = $('#start_date').val();
    let end_date = $('#end_date').val();
    let answer = confirm(`${start_date} ~ ${end_date}의 데이터를 마감 하시겠습니까?`);
    if (answer) {
        start_date = set_yyyymmdd(start_date);
        end_date = set_yyyymmdd(end_date);
        let data = `start_date=${start_date}&end_date=${end_date}`;
        $.ajax({
            url: 'product/order/finish',
            type: 'post',
            data: data,
        }).done(function (data) {
            alert('완료');
            $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        }).fail(function () {
            alert('오류발생! 전산실로 연락 바랍니다.');
        });
    }
});

$("#id_ymd").datepicker({
    autoclose: true,
    format: 'yyyymmdd'
});

$("#createForm form").submit(function (e) {
    e.preventDefault();

    let data = $(this).serialize();
    let type = 'post';
    let url = '/product/order';

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('완료');
        $('#id_count').val('');
        $('#id_amount').val('');
        $('#id_memo').val('');
        $('.django-select2').val('');
        $('.django-select2').trigger('change');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
    }).fail(function () {
        alert('에러발생! 전산팀으로 문의 바랍니다.');
    });
});

$('.has-spinner').click(function () {

    let btn = $(this);
    let form = btn.closest("form");

    if (form[0].checkValidity()) {
        $(btn).buttonLoader('start');
        setTimeout(function () {
            $(btn).buttonLoader('stop');
        }, 1000);
        form.submit();
    }
});

function editButtonClick(data) {
    window.open(`/product/order/popup/${data['id']}`, "PopupWin", "width=530,height=700");
}

AMOUNT_KG = {};
$("#id_productCode").change(function () {

    if ($(this).val()) {
        let pk = $(this).val();

        $.ajax({
            url: '/api/productCodeByPk/' + pk,
            type: 'get',
        }).done(function (data) {
            window.AMOUNT_KG = {"AMOUNT_KG": data["amount_kg"]};
            console.log(window.AMOUNT_KG);
        }).fail(function () {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    }
});

$('#start_date').change(function () {
    $('input[name="ymd"]').val(set_yyyymmdd($('#start_date').val()))
});

$(".amount").focusout(function () {
    setAutoCountValue($(this));
});

$(".count").focusout(function () {
    setAutoAmountValue($(this));
});
