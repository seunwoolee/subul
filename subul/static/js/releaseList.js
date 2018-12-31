 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
     start_date = set_yyyymmdd(start_date);
     end_date = set_yyyymmdd(end_date);
     var LOOKUP_TABLE = {
          "stepOne": function(args) {
            return setStepOneDataTable(args);
          },
          "stepTwo": function() {
            return setStepTwoDataTable(args);
          },
          "stepThree":  function() {
            return setStepThreeDataTable(args);
          },
          "stepFour":  function() {
            return setStepFourDataTable(args);
          },
          "stepFive":  function() {
            return setStepFiveDataTable(args);
          },
          "stepSix":  function() {
            return setStepSixDataTable(args);
          }
     };

     let groupByFilter = $('#tabnavigator a.nav-link.active').attr('href');
     groupByFilter = groupByFilter.substring(1);
     let releaseTypeFilter = $('.type_filter #releaseType select').val();
     let productTypeFilter = $('.type_filter #productType select').val();
     let checkBoxFilter = $('.type_filter input:checkbox:checked').map(function(){ return $(this).val(); })
                                                                  .get().join(',');
     let table = $('#'+groupByFilter +' .datatable');
     args={ 'table' : table,
            'start_date' : start_date,
            'end_date' : end_date,
            'releaseTypeFilter':releaseTypeFilter,
            'productTypeFilter':productTypeFilter,
            'checkBoxFilter':checkBoxFilter,
            'groupByFilter':groupByFilter };
    table.DataTable().destroy();
    LOOKUP_TABLE[groupByFilter](args);
 }

function setStepOneDataTable(args)
{
    table = args['table'].DataTable({
    	"footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;
            let numberFormatWithDot = $.fn.dataTable.render.number( ',', '.', 2).display;
            let numberFormat = $.fn.dataTable.render.number( ',').display;

            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            let pageTotal_amount = api
                .column( 7, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_count = api
                .column( 8, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_pricePerKg = api
                .column( 9, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_price = api
                .column( 10, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_supplyPrice = api
                .column( 11, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_vat = api
                .column( 12, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_pricePerEa = api
                .column( 13, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 7 ).footer() ).html( numberFormatWithDot(pageTotal_amount) + '(KG)' );
            $( api.column( 8 ).footer() ).html( numberFormat(pageTotal_count) + '(EA)' );
            $( api.column( 9 ).footer() ).html( numberFormat(pageTotal_pricePerKg) );
            $( api.column( 10 ).footer() ).html( numberFormat(pageTotal_price) );
            $( api.column( 11 ).footer() ).html( numberFormat(pageTotal_supplyPrice) );
            $( api.column( 12 ).footer() ).html( numberFormat(pageTotal_vat) );
            $( api.column( 13 ).footer() ).html( numberFormat(pageTotal_pricePerEa) );
        },
        "language": {
            "decimal": ",",
            "thousands": "."
        },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date'],
                releaseTypeFilter:args['releaseTypeFilter'],
                productTypeFilter:args['productTypeFilter'],
                checkBoxFilter:args['checkBoxFilter'],
                groupByFilter:args['groupByFilter']
            }
        },
        "responsive" : true,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: 1 },
            { responsivePriority: 3, targets: -1 },
        ],
        "columns": [
            {'data': 'id'},
            {'data': 'ymd'},
            {'data': 'releaseLocationName'},
            {'data': 'contentType'},
            {"data": "specialTag", "render" : function(data, type, row, meta){return setSpecialTagButton(data);}},
            {'data': 'code'},
            {'data': 'codeName'},
            {'data': 'amount' , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'count'},
            {'data': 'kgPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'totalPrice', "render": $.fn.dataTable.render.number( ',')},
            {'data': 'supplyPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'releaseVat' , "render": $.fn.dataTable.render.number( ',')},
            {"data": "eaPrice" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "productYmd"},
            {"data": "type" , "render": function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "releaseStoreLocationCodeName"},
            {"data": "orderMemo"},
            {"data": "memo"},
            {"data": "locationType"},
            {"data": "locationManagerName"},
            {'data': 'releaseSetProduct', "visible": false},
            {'data': 'releaseSetProductCodeName', "visible": false},
            {"data": 'type', "render": function(data, type, row, meta){
                    console.log(data);
                    return setDataTableActionButtonWithPdfRecall();
            }}
        ],
        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'pageLength',
                        className:'btn btn-light',
                        text : '<i class="fas fa-list-ol fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'colvis',
                        className:'btn btn-light',
                        text : '<i class="far fa-eye fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'copy',
                        className:'btn btn-light',
                        text : '<i class="fas fa-copy fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
}

function setStepTwoDataTable(args)
{
    args['table'].DataTable({
    	"footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;
            let numberFormatWithDot = $.fn.dataTable.render.number( ',', '.', 2).display;
            let numberFormat = $.fn.dataTable.render.number( ',').display;

            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            let pageTotal_amount = api
                .column( 5, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_count = api
                .column( 6, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_price = api
                .column( 7, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_pricePerKg = api
                .column( 8, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_supplyPrice = api
                .column( 9, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_vat = api
                .column( 10, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_pricePerEa = api
                .column( 11, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 5 ).footer() ).html( numberFormatWithDot(pageTotal_amount) + '(KG)' );
            $( api.column( 6 ).footer() ).html( numberFormat(pageTotal_count) + '(EA)' );
            $( api.column( 7 ).footer() ).html( numberFormat(pageTotal_price) );
            $( api.column( 8 ).footer() ).html( numberFormat(pageTotal_pricePerKg) );
            $( api.column( 9 ).footer() ).html( numberFormat(pageTotal_supplyPrice) );
            $( api.column( 10 ).footer() ).html( numberFormat(pageTotal_vat) );
            $( api.column( 11 ).footer() ).html( numberFormat(pageTotal_pricePerEa) );
        },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date'],
                releaseTypeFilter:args['releaseTypeFilter'],
                productTypeFilter:args['productTypeFilter'],
                checkBoxFilter:args['checkBoxFilter'],
                groupByFilter:args['groupByFilter']
            }
        },
        "responsive" : true,
        "columns": [
            {'data': 'code'},
            {"data": "specialTag", "render" : function(data, type, row, meta){return setSpecialTagButton(data);}},
            {'data': 'codeName'},
            {"data": "type"},
            {'data': 'contentType'},
            {'data': 'amount' , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'count' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'totalPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'kgPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'supplyPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'releaseVat' , "render": $.fn.dataTable.render.number( ',')},
            {"data": "eaPrice" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "releaseStoreLocationCodeName"}
        ],
        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'pageLength',
                        className:'btn btn-light',
                        text : '<i class="fas fa-list-ol fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'colvis',
                        className:'btn btn-light',
                        text : '<i class="far fa-eye fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'copy',
                        className:'btn btn-light',
                        text : '<i class="fas fa-copy fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
}

function setStepThreeDataTable(args)
{
    args['table'].DataTable({
    	"footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;
            let numberFormatWithDot = $.fn.dataTable.render.number( ',', '.', 2).display;
            let numberFormat = $.fn.dataTable.render.number( ',').display;

            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            let pageTotal_amount = api
                .column( 6, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_count = api
                .column( 7, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_price = api
                .column( 8, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_pricePerKg = api
                .column( 9, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_supplyPrice = api
                .column( 10, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_vat = api
                .column( 11, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_pricePerEa = api
                .column( 12, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 6 ).footer() ).html( numberFormatWithDot(pageTotal_amount) + '(KG)' );
            $( api.column( 7 ).footer() ).html( numberFormat(pageTotal_count) + '(EA)' );
            $( api.column( 8 ).footer() ).html( numberFormat(pageTotal_price) );
            $( api.column( 9 ).footer() ).html( numberFormat(pageTotal_pricePerKg) );
            $( api.column( 10).footer() ).html( numberFormat(pageTotal_supplyPrice) );
            $( api.column( 11 ).footer() ).html( numberFormat(pageTotal_vat) );
            $( api.column( 12 ).footer() ).html( numberFormat(pageTotal_pricePerEa) );
        },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date'],
                releaseTypeFilter:args['releaseTypeFilter'],
                productTypeFilter:args['productTypeFilter'],
                checkBoxFilter:args['checkBoxFilter'],
                groupByFilter:args['groupByFilter']
            }
        },
        "responsive" : true,
        "columns": [
            {'data': 'code'},
            {"data": "specialTag", "render" : function(data, type, row, meta){return setSpecialTagButton(data);}},
            {'data': 'codeName'},
            {"data": "type"},
            {'data': 'releaseLocationName'},
            {'data': 'contentType'},
            {'data': 'amount' , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'count' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'totalPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'kgPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'supplyPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'releaseVat' , "render": $.fn.dataTable.render.number( ',')},
            {"data": "eaPrice" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "releaseStoreLocationCodeName"}
        ],
        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'pageLength',
                        className:'btn btn-light',
                        text : '<i class="fas fa-list-ol fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'colvis',
                        className:'btn btn-light',
                        text : '<i class="far fa-eye fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'copy',
                        className:'btn btn-light',
                        text : '<i class="fas fa-copy fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
}

function setStepFourDataTable(args)
{
    args['table'].DataTable({
    	"footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;
            let numberFormatWithDot = $.fn.dataTable.render.number( ',', '.', 2).display;
            let numberFormat = $.fn.dataTable.render.number( ',').display;

            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            let pageTotal_amount = api
                .column( 1, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_count = api
                .column( 2, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_price = api
                .column( 3, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_supplyPrice = api
                .column( 4, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_vat = api
                .column( 5, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 1 ).footer() ).html( numberFormatWithDot(pageTotal_amount) + '(KG)' );
            $( api.column( 2 ).footer() ).html( numberFormat(pageTotal_count) + '(EA)' );
            $( api.column( 3 ).footer() ).html( numberFormat(pageTotal_price) );
            $( api.column( 4 ).footer() ).html( numberFormat(pageTotal_supplyPrice) );
            $( api.column( 5).footer() ).html( numberFormat(pageTotal_vat) );
        },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date'],
                releaseTypeFilter:args['releaseTypeFilter'],
                productTypeFilter:args['productTypeFilter'],
                checkBoxFilter:args['checkBoxFilter'],
                groupByFilter:args['groupByFilter']
            }
        },
        "responsive" : true,
        "columns": [
            {'data': 'releaseLocationName'},
            {'data': 'amount' , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'count' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'totalPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'supplyPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'releaseVat' , "render": $.fn.dataTable.render.number( ',')},
        ],
        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'pageLength',
                        className:'btn btn-light',
                        text : '<i class="fas fa-list-ol fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'colvis',
                        className:'btn btn-light',
                        text : '<i class="far fa-eye fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'copy',
                        className:'btn btn-light',
                        text : '<i class="fas fa-copy fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
}

function setStepFiveDataTable(args)
{
    args['table'].DataTable({
    	"footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;
            let numberFormatWithDot = $.fn.dataTable.render.number( ',', '.', 2).display;
            let numberFormat = $.fn.dataTable.render.number( ',').display;

            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            let pageTotal_previousStock = api
                .column( 4, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_in = api
                .column( 5, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_sale = api
                .column( 6, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_sample = api
                .column( 7, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_broken = api
                .column( 8, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_notProduct = api
                .column( 9, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_recall = api
                .column( 10, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_currentStock = api
                .column( 11, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 4 ).footer() ).html( numberFormatWithDot(pageTotal_previousStock));
            $( api.column( 5 ).footer() ).html( numberFormatWithDot(pageTotal_in));
            $( api.column( 6 ).footer() ).html( numberFormatWithDot(pageTotal_sale));
            $( api.column( 7 ).footer() ).html( numberFormatWithDot(pageTotal_sample));
            $( api.column( 8 ).footer() ).html( numberFormatWithDot(pageTotal_broken));
            $( api.column( 9 ).footer() ).html( numberFormatWithDot(pageTotal_notProduct));
            $( api.column( 10 ).footer() ).html( numberFormatWithDot(pageTotal_recall));
            $( api.column( 11 ).footer() ).html( numberFormatWithDot(pageTotal_currentStock));
        },
        "language": {
            "lengthMenu": "_MENU_ 페이지당 개수",
            "zeroRecords": "결과 없음",
            "info": "",
            "infoEmpty": "No records available",
            "infoFiltered": "(검색된결과 from _MAX_ total records)"
        },
        "processing": true,
        "serverSide": true,
        "paging": false,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date'],
                releaseTypeFilter:args['releaseTypeFilter'],
                productTypeFilter:args['productTypeFilter'],
                checkBoxFilter:args['checkBoxFilter'],
                groupByFilter:args['groupByFilter']
            }
        },
        "responsive" : true,
        "columns": [
            {'data': 'id'},
            {'data': 'code'},
            {'data': 'codeName'},
            {'data': 'ymd'},
            {'data': 'previousStock', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'in', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'sale', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'sample', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'broken', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'notProduct', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'recall', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'currentStock', "render": $.fn.dataTable.render.number( ',', '.', 2)}
        ],
        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'colvis',
                        className:'btn btn-light',
                        text : '<i class="far fa-eye fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'copy',
                        className:'btn btn-light',
                        text : '<i class="fas fa-copy fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
}

function setStepSixDataTable(args)
{
    args['table'].DataTable({
//    	"footerCallback": function ( row, data, start, end, display ) {
//            var api = this.api(), data;
//            let numberFormatWithDot = $.fn.dataTable.render.number( ',', '.', 2).display;
//            let numberFormat = $.fn.dataTable.render.number( ',').display;
//
//            var intVal = function ( i ) {
//                return typeof i === 'string' ?
//                    i.replace(/[\$,]/g, '')*1 :
//                    typeof i === 'number' ?
//                        i : 0;
//            };
//
//            let pageTotal_previousStock = api
//                .column( 4, { page: 'current'} )
//                .data()
//                .reduce( function (a, b) {
//                    return intVal(a) + intVal(b);
//                }, 0 );
//
//            let pageTotal_in = api
//                .column( 5, { page: 'current'} )
//                .data()
//                .reduce( function (a, b) {
//                    return intVal(a) + intVal(b);
//                }, 0 );
//
//            let pageTotal_sale = api
//                .column( 6, { page: 'current'} )
//                .data()
//                .reduce( function (a, b) {
//                    return intVal(a) + intVal(b);
//                }, 0 );
//
//            let pageTotal_sample = api
//                .column( 7, { page: 'current'} )
//                .data()
//                .reduce( function (a, b) {
//                    return intVal(a) + intVal(b);
//                }, 0 );
//
//            let pageTotal_broken = api
//                .column( 8, { page: 'current'} )
//                .data()
//                .reduce( function (a, b) {
//                    return intVal(a) + intVal(b);
//                }, 0 );
//
//            let pageTotal_notProduct = api
//                .column( 9, { page: 'current'} )
//                .data()
//                .reduce( function (a, b) {
//                    return intVal(a) + intVal(b);
//                }, 0 );
//
//            let pageTotal_recall = api
//                .column( 10, { page: 'current'} )
//                .data()
//                .reduce( function (a, b) {
//                    return intVal(a) + intVal(b);
//                }, 0 );
//
//            let pageTotal_currentStock = api
//                .column( 11, { page: 'current'} )
//                .data()
//                .reduce( function (a, b) {
//                    return intVal(a) + intVal(b);
//                }, 0 );
//
//            // Update footer
//            $( api.column( 4 ).footer() ).html( numberFormatWithDot(pageTotal_previousStock));
//            $( api.column( 5 ).footer() ).html( numberFormatWithDot(pageTotal_in));
//            $( api.column( 6 ).footer() ).html( numberFormatWithDot(pageTotal_sale));
//            $( api.column( 7 ).footer() ).html( numberFormatWithDot(pageTotal_sample));
//            $( api.column( 8 ).footer() ).html( numberFormatWithDot(pageTotal_broken));
//            $( api.column( 9 ).footer() ).html( numberFormatWithDot(pageTotal_notProduct));
//            $( api.column( 10 ).footer() ).html( numberFormatWithDot(pageTotal_recall));
//            $( api.column( 11 ).footer() ).html( numberFormatWithDot(pageTotal_currentStock));
//        },
        "language": {
            "lengthMenu": "_MENU_ 페이지당 개수",
            "zeroRecords": "결과 없음",
            "info": "",
            "infoEmpty": "No records available",
            "infoFiltered": "(검색된결과 from _MAX_ total records)"
        },
        "processing": true,
        "serverSide": true,
        "paging": false,
        "ajax": {
            "url": "/api/release/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date'],
                releaseTypeFilter:args['releaseTypeFilter'],
                productTypeFilter:args['productTypeFilter'],
                checkBoxFilter:args['checkBoxFilter'],
                groupByFilter:args['groupByFilter']
            }
        },
        "responsive" : true,
        "columns": [
            {'data': 'id'},
            {'data': 'locationCode'},
            {'data': 'locationCodeName'},
            {'data': 'productCode'},
            {'data': 'productCodeName'},
            {'data': 'ymd'},
            {'data': 'previousStock', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'in', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'move', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'sale', "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {'data': 'currentStock', "render": $.fn.dataTable.render.number( ',', '.', 2)}
        ],
        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'colvis',
                        className:'btn btn-light',
                        text : '<i class="far fa-eye fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'copy',
                        className:'btn btn-light',
                        text : '<i class="fas fa-copy fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
}

function setDataTableActionButtonWithPdfRecall()
{
    return '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="fa fa-trash-o"></i></button>' +
            '<button class="btn btn-warning btn-sm PDF" href="#"><i class="fas fa-file-pdf"></i></button>' +
            '<button class="btn btn-success btn-sm RECALL" href="#"><i class="fas fa-undo-alt"></i></button>';
}

function setTypeButton(data)
{
    switch(data)
    {
        case '판매':
            return '<button class="btn btn-dark btn-sm">'+ data +'</button>'
            break;
        case '샘플':
            return '<button class="btn btn-warning btn-sm">'+ data +'</button>'
            break;
        case '증정':
            return '<button class="btn btn-success btn-sm">'+ data +'</button>'
            break;
        case '자손':
            return '<button class="btn btn-primary btn-sm ">'+ data +'</button>'
            break;
        case '생산요청':
            return '<button class="btn btn-danger btn-sm">'+ data +'</button>'
            break;
        default : return '<button class="btn btn-primary btn-sm ">'+ data +'</button>';
    }
}

function deleteButtonClick(data)
{
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

function pdfButtonClick(data)
{
    let ymd = data['ymd'];
    let releaseLocationCode = data['releaseLocationCode'];
    window.open('/release/pdf?ymd=' + ymd + '&releaseLocationCode=' + releaseLocationCode, '_blank');
}

var AMOUNT_KG = {};
function editButtonClick(data)
{
    let fakeYmd = set_yyyy_mm_dd(data['ymd']);
    window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"]};
    $('#id_ymd').val(data['ymd']);
    $('#id_fakeYmd').val(fakeYmd);
    $('#id_amount').val(data['amount']);
    $('#id_count').val(data['count']);
    $('#id_price').val(data['price']);
    $('#id_memo').val(data['memo']);
    $('.codeName').text(data['codeName']);
    $("#releaseModal").modal();
}

function recallButtonClick(data)
{
    let fakeYmd = set_yyyy_mm_dd(data['ymd']);
    window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"], "EA_PRICE" : data["eaPrice"]};
    $('#id_ymd_recall').val(data['ymd']);
    $('#id_fakeYmd_recall').val(fakeYmd);
    $('#id_amount_recall').val(data['amount']).attr("max",data['amount']);
    $('#id_count_recall').val(data['count']).attr("max",data['count']);
    $('#id_price_recall').val(data['price']);
    // hiddenFiled
    $('#id_productCode_recall').val(data['code']);
    $('#id_storedLocationCode_recall').val(data['releaseLocationCode']);
    $('#id_productYmd_recall').val(data['productYmd']);
    $('#id_productId_recall').val(data['product_id']);
    $('#id_amount_kg_recall').val(data["amount_kg"]);
    // hiddenFiled
    $('.codeName').text(data['codeName']);
    $("#releaseRecallModal").modal();
}
$("#id_price_recall").click(function(){
    recallCount = $(this).parents('form').find('tr').eq(1).find('#id_count_recall').val();
    $(this).val(window.AMOUNT_KG['EA_PRICE'] * recallCount);
});
$(".amount").focusout(function(){ setAutoCountValue($(this)); });
$(".count").focusout(function(){ setAutoAmountValue($(this)); });
$(".fakeYmd").focusout(function(){
    ymd = set_yyyymmdd($(this).val());
    $('input[name=ymd]').val(ymd);
});

$('form').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();

    if(type != 'post')
    {
        url = '/api/release/'+id;
    }
    else
    {
        url =  '/release/adjustment';
    }

    $.ajax({
    url: url,
    type: type,
    data: data,
    }).done(function(data) {
        alert('수정완료');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});
