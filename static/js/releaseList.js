var LOCATION_MANAGER = false;
$('#start_date').val(start_day);
$('#end_date').val(end_day);
fetch_data(start_day, end_day);

function fetch_data(start_date = '', end_date = '') {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    var LOOKUP_TABLE = {
        "stepOne": function (args) {
            return setStepOneDataTable(args);
        },
        "stepTwo": function () {
            return setStepTwoDataTable(args);
        },
        "stepThree": function () {
            return setStepThreeDataTable(args);
        },
        "stepFour": function () {
            return setStepFourDataTable(args);
        },
        "stepFive": function () {
            return setStepFiveDataTable(args);
        },
        "stepSix": function () {
            return setStepSixDataTable(args);
        }
    };

    let groupByFilter = $('#tabnavigator a.nav-link.active').attr('href');
    groupByFilter = groupByFilter.substring(1);
    let releaseTypeFilter = $('.type_filter #releaseType select').val();
    let productTypeFilter = $('.type_filter #productType select').val();
    let productYmdFilter = $('.type_filter #productYmd input').val();
    if (productYmdFilter) {
        productYmdFilter = set_yyyymmdd(productYmdFilter);
    }
    let checkBoxFilter = $('.type_filter #locationType input:checkbox:checked')
        .not('#moneyMark').map(function () {
            return $(this).val();
        }).get().join(',');
    let table = $('#' + groupByFilter + ' .datatable');
    let locationFilter = $('#locationFilter select').val();
    let managerFilter = $('#managerFilter select').val();
    args = {
        'table': table,
        'start_date': start_date,
        'end_date': end_date,
        'releaseTypeFilter': releaseTypeFilter,
        'productTypeFilter': productTypeFilter,
        'productYmdFilter': productYmdFilter,
        'checkBoxFilter': checkBoxFilter,
        'locationFilter': locationFilter,
        'managerFilter': managerFilter,
        'location_manager': window.LOCATION_MANAGER,
        'groupByFilter': groupByFilter
    };
    table.DataTable().destroy();
    LOOKUP_TABLE[groupByFilter](args);
    $('.customTolltip').tooltip();
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

            let pageTotal_pricePerKg = api
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

            let pageTotal_supplyPrice = api
                .column(11, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_vat = api
                .column(12, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_pricePerEa = api
                .column(13, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(7).footer()).html(numberFormatWithDot(pageTotal_amount) + '(KG)');
            $(api.column(8).footer()).html(numberFormat(pageTotal_count) + '(EA)');
            $(api.column(9).footer()).html(numberFormat(pageTotal_pricePerKg));
            $(api.column(10).footer()).html(numberFormat(pageTotal_price));
            $(api.column(11).footer()).html(numberFormat(pageTotal_supplyPrice));
            $(api.column(12).footer()).html(numberFormat(pageTotal_vat));
            $(api.column(13).footer()).html(numberFormat(pageTotal_pricePerEa));
        },
        "language": {searchPlaceholder: "제품, 메모, 주문메모"},
        "processing": true,
        "serverSide": true,
        "order": [[2, "asc"]],
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date: args['start_date'],
                end_date: args['end_date'],
                releaseTypeFilter: args['releaseTypeFilter'],
                productTypeFilter: args['productTypeFilter'],
                productYmdFilter: args['productYmdFilter'],
                checkBoxFilter: args['checkBoxFilter'],
                locationFilter: args['locationFilter'],
                managerFilter: args['managerFilter'],
                location_manager: args['location_manager'],
                groupByFilter: args['groupByFilter']
            }
        },
        "responsive": true,
        "columnDefs": [
            {responsivePriority: 1, targets: 0},
            {responsivePriority: 2, targets: 1},
            {responsivePriority: 3, targets: -1},
            {targets: 7, className: "dt-body-right"},
            {targets: 8, className: "dt-body-right"},
            {targets: 9, className: "dt-body-right"},
            {targets: 10, className: "dt-body-right"},
            {targets: 11, className: "dt-body-right"},
            {targets: 12, className: "dt-body-right"},
            {targets: 13, className: "dt-body-right"},
        ],
        "columns": [
            {'data': 'releaseLocationName'},
            {"data": "releaseStoreLocationCodeName"},
            {'data': 'ymd'},
            {'data': 'codeName'},
            {"data": "productYmd"},
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
            {'data': 'amounts', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'counts'},
            {'data': 'kgPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'totalPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'supplyPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'releaseVat', "render": $.fn.dataTable.render.number(',')},
            {"data": "eaPrice", "render": $.fn.dataTable.render.number(',')},
            {'data': 'contentType'},
            {"data": "orderMemo"},
            {"data": "memo"},
            {"data": "locationType"},
            {"data": "locationManagerName"},
            {'data': 'releaseSetProduct'},
            {'data': 'releaseSetProductCodeName'},
            {'data': 'id'},
            {'data': 'code'},
            {
                "data": 'type', "render": function (data, type, row, meta) {
                    if (superUserOrfutureData(row.ymd)) {
                        if (row.locationType === '원란판매') {
                            return '';
                        }

                        if (data === '이동') {
                            return setDataTableActionButtonMovePdf();
                        } else if (data === '판매') {
                            return setDataTableActionButtonWithPdfRecall();
                        } else {
                            return setDataTableActionButtonWithoutEdit();
                        }
                    }

                    if (oneMonthBefore(row.ymd)) {
                        if (today <= getMiddleDay(today)) {
                            if (row.locationType === '원란판매') {
                                return '';
                            }

                            if (data === '이동') {
                                return setDataTableActionButtonMovePdf();
                            } else if (data === '판매') {
                                return setDataTableActionButtonWithPdfRecall();
                            } else {
                                return setDataTableActionButtonWithoutEdit();
                            }
                        }
                    }

                    if (nextYearCheck(row.ymd)) {
                        if (row.locationType === '원란판매') {
                            return '';
                        }

                        if (data === '이동') {
                            return setDataTableActionButtonMovePdf();
                        } else if (data === '판매') {
                            return setDataTableActionButtonWithPdfRecall();
                        } else {
                            return setDataTableActionButtonWithoutEdit();
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
    });
}

function setStepTwoDataTable(args) {
    args['table'].DataTable({
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

            let pageTotal_price = api
                .column(7, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_pricePerKg = api
                .column(8, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_supplyPrice = api
                .column(9, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_vat = api
                .column(10, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_pricePerEa = api
                .column(11, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(5).footer()).html(numberFormatWithDot(pageTotal_amount) + '(KG)');
            $(api.column(6).footer()).html(numberFormat(pageTotal_count) + '(EA)');
            $(api.column(7).footer()).html(numberFormat(pageTotal_price));
            $(api.column(8).footer()).html(numberFormat(pageTotal_pricePerKg));
            $(api.column(9).footer()).html(numberFormat(pageTotal_supplyPrice));
            $(api.column(10).footer()).html(numberFormat(pageTotal_vat));
            $(api.column(11).footer()).html(numberFormat(pageTotal_pricePerEa));
        },
        "language": {searchPlaceholder: "제품명, 보관장소"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date: args['start_date'],
                end_date: args['end_date'],
                releaseTypeFilter: args['releaseTypeFilter'],
                productTypeFilter: args['productTypeFilter'],
                checkBoxFilter: args['checkBoxFilter'],
                location_manager: args['location_manager'],
                groupByFilter: args['groupByFilter']
            }
        },
        "responsive": true,
        "columnDefs": [
            {targets: 5, className: "dt-body-right"},
            {targets: 6, className: "dt-body-right"},
            {targets: 7, className: "dt-body-right"},
            {targets: 8, className: "dt-body-right"},
            {targets: 9, className: "dt-body-right"},
            {targets: 10, className: "dt-body-right"},
            {targets: 11, className: "dt-body-right"},
        ],
        "columns": [
            {'data': 'code'},
            {
                "data": "specialTag", "render": function (data, type, row, meta) {
                    return setSpecialTagButton(data);
                }
            },
            {'data': 'codeName'},
            {"data": "type"},
            {'data': 'contentType'},
            {'data': 'amount', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'count', "render": $.fn.dataTable.render.number(',')},
            {'data': 'totalPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'kgPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'supplyPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'releaseVat', "render": $.fn.dataTable.render.number(',')},
            {"data": "eaPrice", "render": $.fn.dataTable.render.number(',')},
            {"data": "releaseStoreLocationCodeName"}
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
    });
}

function setStepThreeDataTable(args) {
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

            let pageTotal_pricePerKg = api
                .column(9, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_supplyPrice = api
                .column(10, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_vat = api
                .column(11, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_pricePerEa = api
                .column(12, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(6).footer()).html(numberFormatWithDot(pageTotal_amount) + '(KG)');
            $(api.column(7).footer()).html(numberFormat(pageTotal_count) + '(EA)');
            $(api.column(8).footer()).html(numberFormat(pageTotal_price));
            $(api.column(9).footer()).html(numberFormat(pageTotal_pricePerKg));
            $(api.column(10).footer()).html(numberFormat(pageTotal_supplyPrice));
            $(api.column(11).footer()).html(numberFormat(pageTotal_vat));
            $(api.column(12).footer()).html(numberFormat(pageTotal_pricePerEa));
        },
        "language": {searchPlaceholder: "거래처, 제품명"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date: args['start_date'],
                end_date: args['end_date'],
                releaseTypeFilter: args['releaseTypeFilter'],
                productTypeFilter: args['productTypeFilter'],
                checkBoxFilter: args['checkBoxFilter'],
                location_manager: args['location_manager'],
                groupByFilter: args['groupByFilter']
            }
        },
        "responsive": true,
        "columnDefs": [
            {targets: 6, className: "dt-body-right"},
            {targets: 7, className: "dt-body-right"},
            {targets: 8, className: "dt-body-right"},
            {targets: 9, className: "dt-body-right"},
            {targets: 10, className: "dt-body-right"},
            {targets: 11, className: "dt-body-right"},
            {targets: 12, className: "dt-body-right"},
        ],
        "columns": [
            {'data': 'code'},
            {
                "data": "specialTag", "render": function (data, type, row, meta) {
                    return setSpecialTagButton(data);
                }
            },
            {'data': 'codeName'},
            {"data": "type"},
            {'data': 'releaseLocationName'},
            {'data': 'contentType'},
            {'data': 'amount', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'count', "render": $.fn.dataTable.render.number(',')},
            {'data': 'totalPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'kgPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'supplyPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'releaseVat', "render": $.fn.dataTable.render.number(',')},
            {"data": "eaPrice", "render": $.fn.dataTable.render.number(',')},
            {"data": "releaseStoreLocationCodeName"}
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
    });
}

function setStepFourDataTable(args) {
    args['table'].DataTable({
        "footerCallback": function (row, data, start, end, display) {
            var api = this.api(), data;

            let pageTotal_amount = api
                .column(1, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_count = api
                .column(2, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_price = api
                .column(3, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_supplyPrice = api
                .column(4, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_vat = api
                .column(5, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(1).footer()).html(numberFormatWithDot(pageTotal_amount) + '(KG)');
            $(api.column(2).footer()).html(numberFormat(pageTotal_count) + '(EA)');
            $(api.column(3).footer()).html(numberFormat(pageTotal_price));
            $(api.column(4).footer()).html(numberFormat(pageTotal_supplyPrice));
            $(api.column(5).footer()).html(numberFormat(pageTotal_vat));
        },
        "language": {searchPlaceholder: "거래처"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date: args['start_date'],
                end_date: args['end_date'],
                releaseTypeFilter: args['releaseTypeFilter'],
                productTypeFilter: args['productTypeFilter'],
                checkBoxFilter: args['checkBoxFilter'],
                location_manager: args['location_manager'],
                groupByFilter: args['groupByFilter']
            }
        },
        "responsive": true,
        "columnDefs": [
            {targets: 1, className: "dt-body-right"},
            {targets: 2, className: "dt-body-right"},
            {targets: 3, className: "dt-body-right"},
            {targets: 4, className: "dt-body-right"},
            {targets: 5, className: "dt-body-right"},
        ],
        "columns": [
            {'data': 'releaseLocationName'},
            {'data': 'amount', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'count', "render": $.fn.dataTable.render.number(',')},
            {'data': 'totalPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'supplyPrice', "render": $.fn.dataTable.render.number(',')},
            {'data': 'releaseVat', "render": $.fn.dataTable.render.number(',')},
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
    });
}

function setStepFiveDataTable(args) {
    args['table'].DataTable({
        "footerCallback": function (row, data, start, end, display) {
            var api = this.api(), data;

            let pageTotal_previousStock = api
                .column(4, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_in = api
                .column(5, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_sale = api
                .column(6, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_sample = api
                .column(7, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_broken = api
                .column(8, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_notProduct = api
                .column(9, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_recall = api
                .column(10, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_adjust = api
                .column(11, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            let pageTotal_currentStock = api
                .column(12, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(4).footer()).html(numberFormatWithDot(pageTotal_previousStock));
            $(api.column(5).footer()).html(numberFormatWithDot(pageTotal_in));
            $(api.column(6).footer()).html(numberFormatWithDot(pageTotal_sale));
            $(api.column(7).footer()).html(numberFormatWithDot(pageTotal_sample));
            $(api.column(8).footer()).html(numberFormatWithDot(pageTotal_broken));
            $(api.column(9).footer()).html(numberFormatWithDot(pageTotal_notProduct));
            $(api.column(10).footer()).html(numberFormatWithDot(pageTotal_recall));
            $(api.column(11).footer()).html(numberFormatWithDot(pageTotal_adjust));
            $(api.column(12).footer()).html(numberFormatWithDot(pageTotal_currentStock));
        },
        "language": {searchPlaceholder: "거래처"},
        "processing": true,
        "serverSide": true,
        "paging": false,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date: args['start_date'],
                end_date: args['end_date'],
                releaseTypeFilter: args['releaseTypeFilter'],
                productTypeFilter: args['productTypeFilter'],
                checkBoxFilter: args['checkBoxFilter'],
                location_manager: args['location_manager'],
                groupByFilter: args['groupByFilter']
            }
        },
        "responsive": true,
        "columnDefs": [
            {targets: 4, className: "dt-body-right"},
            {targets: 5, className: "dt-body-right"},
            {targets: 6, className: "dt-body-right"},
            {targets: 7, className: "dt-body-right"},
            {targets: 8, className: "dt-body-right"},
            {targets: 9, className: "dt-body-right"},
            {targets: 10, className: "dt-body-right"},
            {targets: 11, className: "dt-body-right"},
        ],
        "columns": [
            {'data': 'id'},
            {'data': 'code'},
            {'data': 'codeName'},
            {'data': 'ymd'},
            {'data': 'previousStock', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'in', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'sale', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'sample', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'broken', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'notProduct', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'recall', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'adjust', "render": $.fn.dataTable.render.number(',', '.', 2)},
            {'data': 'currentStock', "render": $.fn.dataTable.render.number(',', '.', 2)}
        ],
        dom: 'Bfrtip',
        buttons: [
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
            return '<button class="btn btn-primary btn-sm ">' + data + '</button>';
    }
}

function deleteButtonClick(data) {
    auditYmd = data['ymd'];
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

function pdfButtonClick(data) {
    let ymd = data['ymd'];
    let releaseLocationCode = data['releaseLocationCodes'];
    let moneyMark = $("#moneyMark").is(":checked");
    window.open('/release/pdf?ymd=' + ymd + '&releaseLocationCode=' + releaseLocationCode + "&moneyMark=" + moneyMark, '_blank');
}

function pdfMoveButtonClick(data) {
    let ymd = data['ymd'];
    let releaseLocationCode = data['releaseLocationCodes'];
    window.open('/release/movePdf?ymd=' + ymd + '&releaseLocationCode=' + releaseLocationCode, '_blank');
}

var AMOUNT_KG = {};

function editButtonClick(data) {
    auditYmd = data['ymd'];
    let fakeYmd = set_yyyy_mm_dd(data['ymd']);
    window.AMOUNT_KG = {"AMOUNT_KG": data["amount_kg"]};
    $('#id_price').val(data['price']);
    $('#id_releaseVat').val(data['releaseVat']);
    $('#id_amount').val(data['amount']);
    $('#id_count').val(data['count']);
    $('#id_orderMemo').val(data['orderMemo']);
    $('#releaseModal .codeName').text(data['codeName']);
    $("#releaseModal").modal();
}

function recallButtonClick(data) {
    auditYmd = data['ymd'];
    let fakeYmd = set_yyyy_mm_dd(data['ymd']);
    window.AMOUNT_KG = {"AMOUNT_KG": data["amount_kg"], "EA_PRICE": data["eaPrice"]};
    $('#id_ymd_recall').val(data['ymd']);
    $('#id_fakeYmd_recall').val(fakeYmd);
    $('#id_amount_recall').val(data['amount']).attr("max", data['amount']);
    $('#id_count_recall').val(data['count']).attr("max", data['count']);
    $('#id_price_recall').val(data['price']);
    // hiddenFiled
    $('#id_productCode_recall').val(data['code']);
    $('#id_storedLocationCode_recall').val(data['releaseLocationCodes']);
    $('#id_productYmd_recall').val(data['productYmd']);
    $('#id_productId_recall').val(data['product_id']);
    $('#id_amount_kg_recall').val(data["amount_kg"]);
    // hiddenFiled
    $('.codeName').text(data['codeName']);
    $("#releaseRecallModal").modal();
}

$("#id_price_recall").click(function () {
    recallCount = $(this).parents('form').find('tr').eq(1).find('#id_count_recall').val();
    $(this).val(window.AMOUNT_KG['EA_PRICE'] * recallCount);
});
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

$('form').on('submit', function (e) {
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();

    if (type != 'post') {
        url = '/api/release/' + id;
    } else {
        url = '/release/adjustment';
    }

    checkAudit(auditYmd)
        .then(r => {
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
        })
        .catch(error => {
            alert(auditMessage);
        })
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

$('.nav-item a').click(function () { // 탭별 style 주기
    let nav_item_id = $(this).attr('href');
    if (nav_item_id == "#stepOne") {
        $('.type_filter #productYmd').show("slow");
        $('.type_filter #managerFilter').show("slow");
        $('.type_filter #locationFilter').show("slow");
    } else {
        $('.type_filter #productYmd').hide("slow");
        $('.type_filter #managerFilter').hide("slow");
        $('.type_filter #locationFilter').hide("slow");
    }
});
