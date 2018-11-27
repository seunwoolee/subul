
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
          }
     };

     let groupByFilter = $('.card-body .tab-content .active').attr('id');
     let releaseTypeFilter = $('.type_filter #releaseType select').val();
     let productTypeFilter = $('.type_filter #productType select').val();
     let checkBoxFilter = $('.type_filter input:checkbox:checked').map(function(){ return $(this).val(); })
                                                                  .get().join(',');
     table = $('#'+groupByFilter +' .datatable');
     args={ 'table' : table,
            'start_date' : start_date,
            'end_date' : end_date,
            'releaseTypeFilter':releaseTypeFilter,
            'productTypeFilter':productTypeFilter,
            'checkBoxFilter':checkBoxFilter,
            'groupByFilter':groupByFilter };
    LOOKUP_TABLE[groupByFilter](args);
 }

function setStepOneDataTable(args)
{
    table = args['table'].DataTable({
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
            {"data": "type"},
            {"data": "releaseStoreLocationCodeName"},
            {"data": "orderMemo"},
            {"data": "locationType"},
            {"data": "locationManagerName"},
            {'data': 'releaseSetProduct', "visible": false},
            {'data': 'releaseSetProductCodeName', "visible": false},
            {"data": null, "render": function(data, type, row, meta){return setDataTableActionButton();}}
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
    table = args['table'].DataTable({
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
        "columns": [
            {'data': 'code'},
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
    table = args['table'].DataTable({
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
        "columns": [
            {'data': 'code'},
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
    table = args['table'].DataTable({
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


var AMOUNT_KG = {};
function editButtonClick(data)
{
    console.log(data);
    window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"]};
    $('#id_ymd').val(data['ymd']);
    $('#id_amount').val(data['amount']);
    $('#id_count').val(data['count']);
    $('#id_price').val(data['price']);
//    $('#id_memo').val(data['memo']); # TODO 메모 있어야댐
    $('.modal_title').text('EDIT');
    $('.codeName').text(data['codeName']);
    $("#releaseModal").modal();
}

$(".amount").focusout(function(){ setAutoCountValue($(this)); });
$(".count").focusout(function(){ setAutoAmountValue($(this)); });

function deleteButtonClick(data)
{
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

$('form').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();
    url = '/api/release/'+id;
    console.log(data);

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
