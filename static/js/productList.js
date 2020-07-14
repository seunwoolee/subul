$('#start_date').val(start_day);
$('#end_date').val(end_day);
fetch_data(start_day, end_day);

function fetch_data(start_date = '', end_date = '') {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let checkBoxFilter = $('.type_filter input:checkbox:checked').map(function () {
        return $(this).val();
    }).get().join(',');
    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "footerCallback": function (row, data, start, end, display) {
            var api = this.api(), data;

            let pageTotal_amount = api
                .column(5, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_count = api
                .column(6, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_rawTank = api
                .column(7, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_pastTank = api
                .column(8, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_loss_insert = api
                .column(9, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_loss_openEgg = api
                .column(10, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_loss_clean = api
                .column(11, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_loss_fill = api
                .column(12, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(5).footer()).html(numberFormatWithDot(pageTotal_amount) + '(KG)');
            $(api.column(6).footer()).html(numberFormat(pageTotal_count) + '(EA)');
            $(api.column(7).footer()).html(numberFormat(pageTotal_rawTank));
            $(api.column(8).footer()).html(numberFormat(pageTotal_pastTank));
            $(api.column(9).footer()).html(numberFormatWithDot(pageTotal_loss_insert));
            $(api.column(10).footer()).html(numberFormatWithDot(pageTotal_loss_openEgg));
            $(api.column(11).footer()).html(numberFormatWithDot(pageTotal_loss_clean));
            $(api.column(12).footer()).html(numberFormatWithDot(pageTotal_loss_fill));
        },
        "responsive": true,
        "columnDefs": [
            {responsivePriority: 1, targets: 0},
            {responsivePriority: 2, targets: -1, orderable: false},
            {responsivePriority: 3, targets: 2},
            {targets: 3, className: "dt-justify"},
            {targets: 4, className: "dt-justify"},
            {targets: 5, className: "dt-body-right"},
            {targets: 6, className: "dt-body-right"},
            {targets: 7, className: "dt-body-right"},
            {targets: 8, className: "dt-body-right"},
            {targets: 9, className: "dt-body-right"},
            {targets: 10, className: "dt-body-right"},
            {targets: 11, className: "dt-body-right"},
            {targets: 12, className: "dt-body-right"},
        ],
        "language": {searchPlaceholder: "제품명, 메모"},
        "select": true,
        "processing": true,
        "serverSide": true,
        "order": [[5, "asc"]],
        "ajax": {
            "url": "/api/product/",
            "type": "GET",
            "data": {
                start_date: start_date, end_date: end_date, checkBoxFilter: checkBoxFilter
            }
        },
        "columns": [
            {"data": "id"},
            {
                "data": "list_type", "render": function (data, type, row, meta) {
                    return setTypeButton(data);
                }
            },
            {"data": "list_code"},
            {"data": "list_codeName"},
            {"data": "list_ymd"},
            {"data": "list_amount", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "list_count", "render": $.fn.dataTable.render.number(',')},
            {"data": "list_rawTank_amount", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "list_pastTank_amount", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "list_loss_insert", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "list_loss_openEgg", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "list_loss_clean", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "list_loss_fill", "render": $.fn.dataTable.render.number(',', '.', 2)},
            {"data": "list_memo"},
            {
                "data": "list_type", "render": function (data, type, row, meta) {

                    if (superUserOrfutureData(row.list_ymd)) {
                        if (data === "제품생산") {
                            return setDataTableActionButtonWithRecall();
                        } else if (data.includes("미출고품")) {
                            return setDataTableActionButtonOnlyDelete();
                        } else {
                            return setDataTableActionButton();
                        }
                    }


                    if (oneMonthBefore(row.list_ymd))
                    {
                        if (today <= getMiddleDay(today)) // 한달전의 1일부터 30일까지 자료는 수정 삭제 가능
                        {
                            if (data === "제품생산") {
                                return setDataTableActionButtonWithRecall();
                            } else if (data.includes("미출고품")) {
                                return setDataTableActionButtonOnlyDelete();
                            } else {
                                return setDataTableActionButton();
                            }
                        }
                    }

                    if (nextYearCheck(row.list_ymd)) {
                        if (data === "제품생산") {
                            return setDataTableActionButtonWithRecall();
                        } else if (data.includes("미출고품")) {
                            return setDataTableActionButtonOnlyDelete();
                        } else {
                            return setDataTableActionButton();
                        }
                    }

                    return "";
                }
            }
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'selectAll',
                className: 'btn btn-light',
                text: '<i class="fas fa-hand-pointer"></i>',
                init: function (api, node, config) {
                    $(node).removeClass('btn-secondary');
                }
            },
            {
                text: '<i class="far fa-trash-alt"></i>',
                className: 'btn btn-light',
                action: deleteSelectedRows
            },
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
            $('td:eq(4)', row).html(set_yyyy_mm_dd(data.list_ymd));
            if (data.list_rawTank_amount < 0) {
                $(row).find('td:eq(7)').css('color', 'red');
            }
            if (data.list_pastTank_amount < 0) {
                $(row).find('td:eq(8)').css('color', 'red');
            }
            if (data.list_amount === 0) {
                $(row).find('td:eq(5)').html('');
            }
            if (data.list_count == 0) {
                $(row).find('td:eq(6)').html('');
            }
            if (data.list_rawTank_amount == 0) {
                $(row).find('td:eq(7)').html('');
            }
            if (data.list_pastTank_amount == 0) {
                $(row).find('td:eq(8)').html('');
            }
            if (data.list_loss_insert == 0) {
                $(row).find('td:eq(9)').html('');
            }
            if (data.list_loss_openEgg == 0) {
                $(row).find('td:eq(10)').html('');
            }
            if (data.list_loss_clean == 0) {
                $(row).find('td:eq(11)').html('');
            }
            if (data.list_loss_fill == 0) {
                $(row).find('td:eq(12)').html('');
            }
        },
        drawCallback: function (settings) {
            $.ajax({
                url: '/api/productSummary',
                type: 'get',
                data: {start_date: start_date, end_date: end_date}
            }).done(function (data) {
                $("#openEggPercent").html(`할란수율 : ${data['openEggPercent']} %`);
                $("#productPercent").html(`제품수율 : ${data['productPercent']} %`);
                $("#lossTotal").html(`로스량 : ${data['lossTotal']} kg`);
                $("#insertLoss").html(`투입LOSS : ${data['insertLoss']} %`);
                $("#openEggLoss").html(`할란LOSS : ${data['openEggLoss']} %`);
            }).fail(function () {
                console.log('수정 에러 전산실로 문의바랍니다(Summary Error).');
            });
            $('[data-toggle="tooltip"]').tooltip();
        }
    });


}

function setTypeButton(data) {
    switch (data) {
        case '할란':
            return '<button class="btn btn-danger btn-sm">' + data + '</button>';
        case '할란사용':
            return '<button class="btn btn-warning btn-sm">' + data + '</button>';
        case '공정품투입':
            return '<button class="btn btn-success btn-sm">' + data + '</button>';
        case '공정품발생':
            return '<button class="btn btn-primary btn-sm ">' + data + '</button>';
        case '공정품폐기':
            return '<button class="btn btn-secondary btn-sm">' + data + '</button>';
        case '제품생산':
            return '<button class="btn btn-dark btn-sm">' + data + '</button>';
        case '미출고품사용':
            return '<button class="btn btn-secondary btn-sm">' + data + '</button>';
        case '미출고품투입':
            return '<button class="btn btn-info btn-sm">' + data + '</button>';
    }
}

var AMOUNT_KG = {};

function editButtonClick(data) {
    if (data['list_type'] == "제품생산") {
        window.AMOUNT_KG = {"AMOUNT_KG": data["list_amount_kg"]};
        $('#amount').val(data['list_amount']);
        $('#count').val(data['list_count']);
        $('.memo').val(data['list_memo']);
        $('.modal_title').text('EDIT');
        $('.codeName').text(data['list_codeName']);
        $('.productType').val('product');
        $("#productModal").modal();
    } else // 할란, 할란사용, 공정품투입, 공정품발생
    {
        if (data['list_codeName'].indexOf('RAW') != -1) {
            tank_amount = data['list_rawTank_amount'];
            $('#tank_amount').val(tank_amount).attr("name", "rawTank_amount");
        } else {
            tank_amount = data['list_pastTank_amount'];
            $('#tank_amount').val(tank_amount).attr("name", "pastTank_amount");
        }
        $('.productType').val('productEgg');
        $('.memo').val(data['list_memo']);
        $('.type').val('edit');
        $('.modal_title').text('EDIT');
        $('.codeName').text(data['list_codeName']);
        $("#productEggModal").modal();
    }
}

function deleteButtonClick(data) {
    let code = data['list_code'];
    let codeHash = {'01201': '01201', '01202': '01202', '01203': '01203'}; // RAW TANK 코드
    let FALG = codeHash[code];

    if (data['list_type'] == "제품생산" || (data['list_type'] == "미출고품사용" && FALG === undefined)) {
        $('.productType').val('product');
    } else {
        $('.productType').val('productEgg');
    }
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

function recallButtonClick(data) {
    window.AMOUNT_KG = {"AMOUNT_KG": data["list_amount_kg"]};
    $('#id_amount_recall').val(data['list_amount']).attr("max", data['list_amount']);
    $('#id_count_recall').val(data['list_count']).attr("max", data['list_count']);
    $('.codeName').text(data['list_codeName']);
    $("#releaseRecallModal").modal();
}

$('form').on('submit', function (e) {
    e.preventDefault();
    $this = $(this);
    let data = $this.serialize();
    let type = $this.find('.ajaxUrlType').val();
    url = setAjaxUrl($this);

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('완료');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function (e) {
        if (e.status == 403) {
            alert('재고를 확인해 주세요');
        } else {
            alert('수정 에러 전산실로 문의바랍니다.');
        }
    });
});

function setAjaxUrl($this) {
    let productType = $this.find("input[name='productType']").val();
    if (productType == 'product') {
        url = '/api/product/' + id;
    } else if (productType == 'productEgg') {
        url = '/api/productEgg/' + id;
    } else if (productType == 'recall') {
        url = '/product/recall/' + id;
    }
    return url;
}

$(".amount").focusout(function () {
    setAutoCountValue($(this));
});
$(".count").focusout(function () {
    setAutoAmountValue($(this));
});
$(".fakeYmd").focusout(function () {
    ymd = set_yyyymmdd($(this).val());
    $('input[name=ymd]').val(ymd);
});

$("#productReport").click(function () {
    let start_date = set_yyyymmdd($('#start_date').val());
    let end_date = set_yyyymmdd($('#end_date').val());
    window.open('/product/productReport?start_date=' + start_date + '&end_date=' + end_date);
});

function deleteSelectedRows() {

    const minYmd = Math.min(...table.rows('.selected').data().toArray().map(row => row.list_ymd));
    if(minYmd < minusFifteen_day){
        alert('15일 전의 데이터는 일괄 삭제 할 수 없습니다.');
        return;
    }

    if(confirm('삭제하시겠습니까?')) {
        let codeHash = {'01201': '01201', '01202': '01202', '01203': '01203'}; // RAW TANK 코드
        let selectedRows = table.rows('.selected').data();
        let product_data = [];
        let productEgg_data = [];

        $.each(selectedRows, function( index, row ) {
            let code = row['list_code'];
            let FALG = codeHash[code];

            if (row['list_type'] === "제품생산" || (row['list_type'] === "미출고품사용" && FALG === undefined)) {
                product_data.push(row.id)
            } else {
                productEgg_data.push(row.id)
            }
        });

        if(product_data.length > 0 || productEgg_data.length > 0) {
            $.ajax({
                url: '/api/product/deleteSelectedRows',
                type: 'delete',
                data: {'product_data[]': product_data, 'productEgg_data[]': productEgg_data},
            }).done(function (data) {
                alert('완료');
                $('.datatable').DataTable().search($("input[type='search']").val()).draw();
                $(".everyModal").modal('hide');
            }).fail(function (e) {
                alert('수정 에러 전산실로 문의바랍니다.');
            });
        } else {
            alert('삭제할 대상을 선택해주세요.');
        }
    }
}
