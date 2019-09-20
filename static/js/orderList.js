var LOCATION_MANAGER = false;
$('#start_date').val(end_day);
$('#end_date').val(plusThree_day);
fetch_data(end_day, plusThree_day);

function fetch_data(start_date = '', end_date = '') {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let LOOKUP_TABLE = {
        "stepOne": function (args) {
            return setStepOneDataTable(args);
        },
        "stepTwo": function (args) {
            return setStepTwoDataTable(args);
        }
    };

    let gubunFilter = $('#tabnavigator a.nav-link.active').attr('href');
    gubunFilter = gubunFilter.substring(1);
    let checkBoxFilter = $('.type_filter input:checkbox:checked').not('#moneyMark')
        .map(function () {
            return $(this).val();
        }).get().join(',');
    let table = $('#' + gubunFilter + ' .datatable');
    let locationFilter = $('#locationFilter select').val();
    let managerFilter = $('#managerFilter select').val();
    var args = {
        'table': table,
        'start_date': start_date,
        'end_date': end_date,
        'checkBoxFilter': checkBoxFilter,
        'locationFilter': locationFilter,
        'managerFilter': managerFilter,
        'location_manager': window.LOCATION_MANAGER,
        'gubunFilter': gubunFilter
    };
    table.DataTable().destroy();
    LOOKUP_TABLE[gubunFilter](args);
}

function setStepOneDataTable(args) {
    table = args['table'].DataTable({
        "footerCallback": function (row, data, start, end, display) {
            var api = this.api(), data;

            let pageTotal_amount = api
                .column(7, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_count = api
                .column(8, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_pricePerEa = api
                .column(9, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_price = api
                .column(10, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(7).footer()).html(numberFormatWithDot(pageTotal_amount) + '(KG)');
            $(api.column(8).footer()).html(numberFormat(pageTotal_count) + '(EA)');
            $(api.column(9).footer()).html(numberFormat(pageTotal_pricePerEa));
            $(api.column(10).footer()).html(numberFormat(pageTotal_price));
        },
        "language": {searchPlaceholder: "제품명, 메모"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": {
                start_date: args['start_date'],
                end_date: args['end_date'],
                checkBoxFilter: args['checkBoxFilter'],
                locationFilter: args['locationFilter'],
                managerFilter: args['managerFilter'],
                location_manager: args['location_manager'],
                gubunFilter: args['gubunFilter']
            }
        },
        "responsive": true,
        "columnDefs": [
            {responsivePriority: 1, targets: 0},
            {responsivePriority: 2, targets: 3},
            {responsivePriority: 3, targets: -1, orderable: false},
            {targets: 4, orderable: false},
            {targets: 7, className: "dt-body-right"},
            {targets: 8, className: "dt-body-right"},
            {targets: 9, className: "dt-body-right"},
            {targets: 10, className: "dt-body-right"}
        ],
        "columns": [
            {"data": "id"},
            {
                "data": "type", "render": function (data, type, row, meta) {
                    return setTypeButton(data);
                }
            },
            {
                "data": "specialTag", "render": function (data, type, row, meta) {
                    return setSpecialTagButton(data);
                }
            },
            {"data": "ymd"},
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
            {"data": "setProduct"},
            {
                "data": "release_id", "render": function (data, type, row, meta) {

                    if (SUPERUSER || getYearMonth(row.ymd) >= getYearMonth(today)) {
                        if (data > 0) {
                            return setDataTableActionButtonWithoutEdit();
                        } else {
                            return setDataTableActionButtonWithPdf();
                        }
                    }


                    if (getYear(row.ymd) == getYear(today) && getMonth(row.ymd) == getMonth(today) - 1) {
                        if (today <= getMiddleDay(today)) {
                            if (data > 0) {
                                return setDataTableActionButtonWithoutEdit();
                            } else {
                                return setDataTableActionButtonWithPdf();
                            }
                        }
                    }

                    return setDataTableActionButtonOnlyPdf();
                }
            }
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'pageLength',
                className: 'btn btn-light',
                text: '<i class="fas fa-list-ol fa-lg"></i>',
                init: function (api, node, config) {
                    $(node).removeClass('btn-secondary');
                }
            },
            {
                extend: 'colvis',
                className: 'btn btn-light',
                text: '<i class="far fa-eye fa-lg"></i>',
                init: function (api, node, config) {
                    $(node).removeClass('btn-secondary');
                }
            },
            {
                extend: 'excel',
                footer: true,
                className: 'btn btn-light',
                text: '<i class="far fa-file-excel fa-lg"></i>',
                init: function (api, node, config) {
                    $(node).removeClass('btn-secondary');
                }
            }],
        lengthMenu: [[-1, 100], ["All", 100]],
        rowCallback: function (row, data, index) {
            $('td:eq(3)', row).html(set_yyyy_mm_dd(data.ymd));
        }
    });
}

function setStepTwoDataTable(args) {
    args['table'].DataTable({
        "footerCallback": function (row, data, start, end, display) {
            var api = this.api(), data;

            let pageTotal_amount = api
                .column(6, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_count = api
                .column(7, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_price = api
                .column(8, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_release_amount = api
                .column(10, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_release_count = api
                .column(11, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_release_price = api
                .column(12, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(6).footer()).html(numberFormatWithDot(pageTotal_amount) + '(KG)');
            $(api.column(7).footer()).html(numberFormat(pageTotal_count) + '(EA)');
            $(api.column(8).footer()).html(numberFormat(pageTotal_price));
            $(api.column(10).footer()).html(numberFormat(pageTotal_release_amount) + '(KG)');
            $(api.column(11).footer()).html(numberFormat(pageTotal_release_count) + '(EA)');
            $(api.column(12).footer()).html(numberFormat(pageTotal_release_price));
        },
        "language": {searchPlaceholder: "제품명"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": {
                start_date: args['start_date'],
                end_date: args['end_date'],
                checkBoxFilter: args['checkBoxFilter'],
                locationFilter: args['locationFilter'],
                managerFilter: args['managerFilter'],
                location_manager: args['location_manager'],
                gubunFilter: args['gubunFilter']
            }
        },
        "responsive": true,
        "columnDefs": [
            {responsivePriority: 1, targets: 0},
            {responsivePriority: 2, targets: 1},
            {responsivePriority: 3, targets: 3},
            {targets: 6, className: "dt-body-right"},
            {targets: 7, className: "dt-body-right"},
            {targets: 8, className: "dt-body-right"},
            {targets: 10, className: "dt-body-right"},
            {targets: 11, className: "dt-body-right"},
            {targets: 12, className: "dt-body-right"},
        ],
        "columns": [
            {"data": "order_id"},
            {
                "data": "order_type", "render": function (data, type, row, meta) {
                    return setTypeButton(data);
                }
            },
            {
                "data": "order_specialTag", "render": function (data, type, row, meta) {
                    return setSpecialTagButton(data);
                }
            },
            {"data": "order_ymd"},
            {"data": "order_orderLocationName"},
            {"data": "order_codeName"},
            {"data": "order_amount", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "order_count", "render": $.fn.dataTable.render.number(',')},
            {"data": "order_totalPrice", "render": $.fn.dataTable.render.number(',')},
            {
                "data": "release_ymd", "render": function (data, type, row, meta) {
                    return setRelease_ymd(data);
                }
            },
            {"data": "release_amount", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "release_count", "render": $.fn.dataTable.render.number(',')},
            {"data": "release_totalPrice", "render": $.fn.dataTable.render.number(',')},
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'pageLength',
                className: 'btn btn-light',
                text: '<i class="fas fa-list-ol fa-lg"></i>',
                init: function (api, node, config) {
                    $(node).removeClass('btn-secondary');
                }
            },
            {
                extend: 'colvis',
                className: 'btn btn-light',
                text: '<i class="far fa-eye fa-lg"></i>',
                init: function (api, node, config) {
                    $(node).removeClass('btn-secondary');
                }
            },
            {
                extend: 'excel',
                footer: true,
                className: 'btn btn-light',
                text: '<i class="far fa-file-excel fa-lg"></i>',
                init: function (api, node, config) {
                    $(node).removeClass('btn-secondary');
                }
            }],
        lengthMenu: [[-1, 100], ["All", 100]],
        rowCallback: function (row, data, index) {
            $('td:eq(3)', row).html(set_yyyy_mm_dd(data.ymd));
            $('td:eq(9)', row).html(set_yyyy_mm_dd(data.release_ymd)).css('color', 'blue');
            if (data.release_totalPrice == 0) {
                $('td:eq(12)', row).html('');
            }

            if (data.release_count == 0 || data.release_amount == 0) {
                $('td:eq(10)', row).html('');
                $('td:eq(11)', row).html('');
            } else if (data.release_count != data.order_count || data.release_amount != data.order_amount) {
                $('td:eq(10)', row).html(data.release_amount).css('color', 'red');
                $('td:eq(11)', row).html(data.release_count).css('color', 'red');
            }

        }
    });
}

function setRelease_ymd(data) {
    if (data != null) {
        return '<span style="color : #2258fb;" ">' + data + '</span>';
    } else {
        return '';
    }
}

function setTypeButton(data) {
    switch (data) {
        case '판매':
            return '<button class="btn btn-dark btn-sm">' + data + '</button>'
            break;
        case '샘플':
            return '<button class="btn btn-warning btn-sm">' + data + '</button>'
            break;
        case '증정':
            return '<button class="btn btn-success btn-sm">' + data + '</button>'
            break;
        case '자손':
            return '<button class="btn btn-primary btn-sm ">' + data + '</button>'
            break;
        case '생산요청':
            return '<button class="btn btn-danger btn-sm">' + data + '</button>'
            break;
        default :
            return ''
    }
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

var AMOUNT_KG = {};
function editButtonClick(data) {
    if (data['release_id'] > 0) {
        alert('출고된 주문내역은 수정할 수 없습니다.');
        return false;
    } else {
        let fakeYmd = set_yyyy_mm_dd(data['ymd']);
        window.AMOUNT_KG = {"AMOUNT_KG": data["amount_kg"], "productCode": data["code"], "locationCode": data["orderLocationCode"]};
        $('#id_ymd').val(data['ymd']);
        $('#id_fakeYmd').val(fakeYmd);
        $('#id_type').val(data['type']);
        $('#id_specialTag').val(data['specialTag']);
        $('#id_amount').val(data['amount']);
        $('#id_count').val(data['count']);
        $('#id_price').val(data['price']);
        $('#id_memo').val(data['memo']);
        $('.modal_title').text('EDIT');
        $('.codeName').text(data['codeName']);
        $("#orderModal").modal();
    }
}

$(".amount").focusout(function () {
    setAutoCountValue($(this));
});
$(".count").focusout(function () {
    setAutoAmountValue($(this));
});
$(".fakeYmd").focusout(function () {
    ymd = set_yyyymmdd($('input[name=fakeYmd]').val());
    $('input[name=ymd]').val(ymd);
});

function deleteButtonClick(data) {
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

function pdfButtonClick(data) {
    let ymd = data['ymd'];
    let orderLocationCode = data['orderLocationCode'];
    let moneyMark = $("#moneyMark").is(":checked");
    window.open('/order/pdf?ymd=' + ymd + '&orderLocationCode=' + orderLocationCode + "&moneyMark=" + moneyMark, '_blank');
}

$('form').on('submit', function (e) {
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();
    url = '/api/order/' + id;

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('수정완료');
        $('#stepOne .datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function () {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

$('#id_specialTag').change(function () {
    let specialTag = $(this).val();

    $.ajax({
        url: "/api/orderPriceMatch/",
        type: "get",
        data: {
            productCode: window.AMOUNT_KG['productCode'],
            locationCode: window.AMOUNT_KG['locationCode']
        },
    }).done(function (data) {
        let price = data.results[0]['price'];
        let specialPrice = data.results[0]['specialPrice'];

        if(specialTag === '특인가'){
            $('#id_price').val(specialPrice);
        } else {
            $('#id_price').val(price);
        }
    }).fail(function () {
        alert('수정 에러 전산실로 문의바랍니다.');
    });

});

$('.nav-item a').click(function () { // 탭별 style 주기
    let nav_item_id = $(this).attr('href');
    if (nav_item_id == "#stepTwo") {
        $('#locationFilter').show('slow');
        $('#managerFilter').show('slow');
        $("#moneyMarkFilter").show('slow');
        $("#characterFilter").show('slow');
        $('#locationManagerSearch').show('slow');
    } else {
        $('#locationFilter').show('slow');
        $('#managerFilter').show('slow');
        $("#moneyMarkFilter").show('slow');
        $("#characterFilter").show('slow');
        $('#locationManagerSearch').show('slow');
    }
});

$('#locationManagerSearch').click(function () {
    window.LOCATION_MANAGER = true;
    var start_date = $('#start_date').val();
    var end_date = $('#end_date').val();
    if (start_date != '' && end_date != '') {
        fetch_data(start_date, end_date);
    } else {
        alert("날짜를 모두 입력해주세요");
    }
});
