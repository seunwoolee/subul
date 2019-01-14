 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let LOOKUP_TABLE = {
        "stepOne": function(args) {
            return setStepOneDataTable(args);
        },
        "stepTwo": function(args) {
            return setStepTwoDataTable(args);
        },
        "stepThree": function(args) {
            return setStepThreeDataTable(args);
        },
    };

    let gubunFilter = $('#tabnavigator a.nav-link.active').attr('href');
    gubunFilter = gubunFilter.substring(1);
    let eggTypeFilter = $('.type_filter #releaseType select').val();
    let checkBoxFilter = $('.type_filter input:checkbox:checked').not('#moneyMark')
                                .map(function(){ return $(this).val(); }).get().join(',');
    let table = $('#'+gubunFilter +' .datatable');
    var args={
            'table' : table,
            'start_date' : start_date,
            'end_date' : end_date,
            'eggTypeFilter':eggTypeFilter,
            'checkBoxFilter':checkBoxFilter,
            'gubunFilter':gubunFilter };
    table.DataTable().destroy();
    LOOKUP_TABLE[gubunFilter](args);
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

            let pageTotal_pricePerEa = api
                .column( 8, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_price = api
                .column( 9, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 6 ).footer() ).html( numberFormatWithDot(pageTotal_amount) + '(KG)' );
            $( api.column( 7 ).footer() ).html( numberFormat(pageTotal_count) + '(EA)' );
            $( api.column( 8 ).footer() ).html( numberFormat(pageTotal_pricePerEa) );
            $( api.column( 9 ).footer() ).html( numberFormat(pageTotal_price) );
        },
        "language": {searchPlaceholder: "거래처, 제품명, 메모"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": {
                        start_date:args['start_date'],
                        end_date:args['end_date'],
                        checkBoxFilter:args['checkBoxFilter'],
                        gubunFilter:args['gubunFilter']
            }
        },
         "createdRow": function( row, data, dataIndex ) {
            $( row ).find('td:eq(0)').attr('data-title','ID');
            $( row ).find('td:eq(1)').attr('data-title','구분');
            $( row ).find('td:eq(2)').attr('data-title','특인');
            $( row ).find('td:eq(3)').attr('data-title','주문일');
            $( row ).find('td:eq(4)').attr('data-title','거래처명');
            $( row ).find('td:eq(5)').attr('data-title','품명');
            $( row ).find('td:eq(6)').attr('data-title','양(KG)');
            $( row ).find('td:eq(7)').attr('data-title','개수(EA)');
            $( row ).find('td:eq(8)').attr('data-title','단가');
            $( row ).find('td:eq(9)').attr('data-title','금액');
            $( row ).find('td:eq(10)').attr('data-title','메모');
            $( row ).find('td:eq(11)').attr('data-title','세트명');
            $( row ).find('td:eq(12)').attr('data-title','Actions');
         },
        "responsive" : true,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: 3 },
            { responsivePriority: 3, targets: -1, orderable: false },
        ],
        "columns": [
            {"data": "id"},
            {"data": "type", "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "specialTag", "render" : function(data, type, row, meta){return setSpecialTagButton(data);}},
            {"data": "ymd"},
            {"data": "orderLocationName"},
            {"data": "codeName"},
            {"data": "amount" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "count" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "price" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "totalPrice" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "memo"},
            {"data": "setProduct"},
            {"data": "release_id", "render": function(data, type, row, meta){
                    if(data > 0)
                    {
                        return setDataTableActionButtonWithoutEdit();
                    }
                    else
                    {
                        return setDataTableActionButtonWithPdf();
                    }
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

            let pageTotal_release_amount = api
                .column( 12, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_release_count = api
                .column( 13, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_release_price = api
                .column( 14, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 6 ).footer() ).html( numberFormatWithDot(pageTotal_amount) + '(KG)' );
            $( api.column( 7 ).footer() ).html( numberFormat(pageTotal_count) + '(EA)' );
            $( api.column( 12 ).footer() ).html( numberFormatWithDot(pageTotal_release_amount) + '(KG)' );
            $( api.column( 13 ).footer() ).html( numberFormat(pageTotal_release_count) + '(EA)' );
            $( api.column( 14 ).footer() ).html( numberFormat(pageTotal_release_price) );
        },
        "language": {searchPlaceholder: "거래처, 제품명"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": {
                        start_date:args['start_date'],
                        end_date:args['end_date'],
                        checkBoxFilter:args['checkBoxFilter'],
                        gubunFilter:args['gubunFilter']
            }
        },
         "createdRow": function( row, data, dataIndex ) {
            $( row ).find('td:eq(0)').attr('data-title','ID');
            $( row ).find('td:eq(1)').attr('data-title','구분');
            $( row ).find('td:eq(2)').attr('data-title','특인');
            $( row ).find('td:eq(3)').attr('data-title','주문일');
            $( row ).find('td:eq(4)').attr('data-title','거래처명');
            $( row ).find('td:eq(5)').attr('data-title','품명');
            $( row ).find('td:eq(6)').attr('data-title','양(KG)');
            $( row ).find('td:eq(7)').attr('data-title','개수(EA)');
            $( row ).find('td:eq(8)').attr('data-title','단가');
            $( row ).find('td:eq(9)').attr('data-title','금액');
            $( row ).find('td:eq(10)').attr('data-title','메모');
            $( row ).find('td:eq(11)').attr('data-title','세트명');
            $( row ).find('td:eq(12)').attr('data-title','Actions');
            $( row ).find('td:eq(13)').attr('data-title','Actions');
            $( row ).find('td:eq(14)').attr('data-title','Actions');
            $( row ).find('td:eq(15)').attr('data-title','Actions');
         },
        "responsive" : true,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: 1 },
            { responsivePriority: 3, targets: 3 },
        ],
        "columns": [
            {"data": "id"},
            {"data": "type", "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "specialTag", "render" : function(data, type, row, meta){return setSpecialTagButton(data);}},
            {"data": "ymd"},
            {"data": "orderLocationName"},
            {"data": "codeName"},
            {"data": "amount" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "count" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "release_ymd" , "render" : function(data, type, row, meta){return setRelease_ymd(data);}},
            {"data": "release_type" , "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "release_locationName"},
            {"data": "release_codeName"},
            {"data": "release_amount" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "release_count" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "release_price" , "render": $.fn.dataTable.render.number( ',')},
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
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date'],
                eggTypeFilter:args['eggTypeFilter'],
                gubunFilter:args['gubunFilter']
            }
        },
        "columns": [
            {'data': 'id'},
            {'data': 'ymd'},
            {'data': 'releaseLocationName'},
            {'data': 'code'},
            {'data': 'codeName'},
            {"data": "count", "render": $.fn.dataTable.render.number( ',')},
            {"data": "amount", "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "price" , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'supplyPrice' , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'releaseVat' , "render": $.fn.dataTable.render.number( ',')}
        ],
        responsive : true,
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

function setRelease_ymd(data)
{
    if(data != null)
    {
       return '<span style="color : #2258fb;" ">'+ data +'</span>';
    }
    else
    {
        return '';
    }
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
        default :
            return ''
    }
}

var AMOUNT_KG = {};
function editButtonClick(data)
{
    if(data['release_id'] > 0)
    {
        alert('출고된 주문내역은 수정할 수 없습니다.');
        return false;
    }
    else
    {
        let fakeYmd = set_yyyy_mm_dd(data['ymd']);
        window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"]};
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

$(".amount").focusout(function(){ setAutoCountValue($(this)); });
$(".count").focusout(function(){ setAutoAmountValue($(this)); });
$(".fakeYmd").focusout(function(){
    ymd = set_yyyymmdd($('input[name=fakeYmd]').val());
    $('input[name=ymd]').val(ymd);
});

function deleteButtonClick(data)
{
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

function pdfButtonClick(data)
{
    let ymd = data['ymd'];
    let orderLocationCode = data['orderLocationCode'];
    let moneyMark = $("#moneyMark").is(":checked");
    window.open('/order/pdf?ymd=' + ymd + '&orderLocationCode=' + orderLocationCode + "&moneyMark=" + moneyMark, '_blank');
}

$('form').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();
    url = '/api/order/'+id;

    $.ajax({
    url: url,
    type: type,
    data: data,
    }).done(function(data) {
        alert('수정완료');
        $('#stepOne .datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});


$('.nav-item a').click(function(){ // 탭별 style 주기
    let nav_item_id = $(this).attr('href');
    $('.type_filter input:checkbox').attr("disabled", true);
    $('.type_filter select').attr("disabled", true);
    if (nav_item_id == "#stepThree")
    {
        $('.type_filter input:checkbox').attr("disabled", true);
        $(".type_filter select").removeAttr("disabled").val('전체');
    }
    else
    {
        $(".type_filter input:checkbox").removeAttr("disabled");
        $('.type_filter select').attr("disabled", true);
    }
});