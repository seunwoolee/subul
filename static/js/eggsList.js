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
          }
     };

    let gubunFilter = $('#tabnavigator a.nav-link.active').attr('href');
    gubunFilter = gubunFilter.substring(1);
    let releaseTypeFilter = $('.type_filter #releaseType_List select').val();
    let productTypeFilter = $('.type_filter #releaseProduct_List select').val();
    let locatoinTypeFilter = $('.type_filter #releaseLocation_List select').val();
    let table = $('#'+gubunFilter +' .datatable');
    var args={
            'table' : table,
            'start_date' : start_date,
            'end_date' : end_date,
            'releaseTypeFilter':releaseTypeFilter,
            'productTypeFilter':productTypeFilter,
            'locatoinTypeFilter':locatoinTypeFilter,
             'gubunFilter': gubunFilter };
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

            let pageTotal_count = api
                .column( 7, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_amount = api
                .column( 8, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_in_price = api
                .column( 9, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_out_price = api
                .column( 10, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 7 ).footer() ).html( numberFormat(pageTotal_count));
            $( api.column( 8 ).footer() ).html( numberFormat(pageTotal_amount));
            $( api.column( 9 ).footer() ).html( numberFormat(pageTotal_in_price) );
            $( api.column( 10 ).footer() ).html( numberFormat(pageTotal_out_price) );
        },
        "language": {searchPlaceholder: "판매처명, 메모"},
        "select": true,
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/eggsList/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date'],
                releaseTypeFilter:args['releaseTypeFilter'],
                productTypeFilter:args['productTypeFilter'],
                locatoinTypeFilter:args['locatoinTypeFilter'],
                gubunFilter:args['gubunFilter']
                }
        },
        "responsive" : true,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: 3 },
            { responsivePriority: 3, targets: -1, orderable: false },
            { targets: 7, className: "dt-body-right"  },
            { targets: 8, className: "dt-body-right"  },
            { targets: 9, className: "dt-body-right"  },
            { targets: 10, className: "dt-body-right"  },
            { targets: 11, className: "dt-body-right"  },
        ],
        "columns": [
            {"data": "id"},
            {"data": "type", "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "in_ymd"},
            {"data": "codeName"},
            {"data": "in_locationCodeName"},
            {"data": "locationCodeName"},
            {"data": "ymd"},
            {"data": "counts" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "amount" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "in_price" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "out_price" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "pricePerEa" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "memo"},
            {"data": "type", "render": function(data, type, row, meta){
                    if(data == "판매") { return setDataTableActionButtonWithPdf(); }
                    else { return setDataTableActionButton(); }
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
        lengthMenu : [[30, 50, -1], [30, 50, "All"]],
        rowCallback: function(row, data, index){
             $('td:eq(2)', row).html( set_yyyy_mm_dd(data.in_ymd) );
             $('td:eq(6)', row).html( set_yyyy_mm_dd(data.ymd) );
            if(data.in_price ==  0){ $(row).find('td:eq(9)').html('') };
            if(data.out_price ==  0){ $(row).find('td:eq(10)').html('') };
        }

    });
}

function setStepTwoDataTable(args)
{
    releaseTable = args['table'].DataTable({
        "language": {searchPlaceholder: "제품명, 농장명"},
        "paging": false,
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/eggs/",
            "type": "GET"
        },
        "responsive" : true,
        "columnDefs": [
            { targets: 3, className: "dt-body-right"  },
        ],
        "columns": [
            {"data": "egg_in_locationCodeName"},
            {"data": "egg_codeName"},
            {"data": "egg_in_ymd"},
            {"data": "totalCount" , "render": $.fn.dataTable.render.number( ',')},
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
        lengthMenu : [[30, 50, -1], [30, 50, "All"]],
        rowCallback: function(row, data, index){
             $('td:eq(2)', row).html( set_yyyy_mm_dd(data.egg_in_ymd) );
        }
    });
}

function setStepThreeDataTable(args)
{
    eggReportTable = args['table'].DataTable({
        "language": {searchPlaceholder: "제품명, 메모"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/eggsReport/",
            "type": "GET",
            "data": {
                start_date:args['start_date'],
                end_date:args['end_date']
                }
        },
        "columns": [
            {"data": "codeName"},
            {"data": "in_ymd"},
            {"data": "in_locationCodeName"},
            {"data": "previousStock" , "render": $.fn.dataTable.render.number( ',')},
            {'data': 'in', "render": $.fn.dataTable.render.number( ',')},
            {'data': 'in_price', "render": $.fn.dataTable.render.number( ',')},
            {'data': 'sale', "render": $.fn.dataTable.render.number( ',')},
            {'data': 'sale_price', "render": $.fn.dataTable.render.number( ',')},
            {'data': 'loss', "render": $.fn.dataTable.render.number( ',')},
            {'data': 'insert', "render": $.fn.dataTable.render.number( ',')},
            {'data': 'release', "render": $.fn.dataTable.render.number( ',')},
            {'data': 'currentStock', "render": $.fn.dataTable.render.number( ',')}
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
        lengthMenu : [[30, 50, -1], [30, 50, "All"]],
        rowCallback: function(row, data, index){
             $('td:eq(1)', row).html( set_yyyy_mm_dd(data.in_ymd) );
        }
    });
}

function setTypeButton(data)
{
    switch(data)
    {
        case '입고':
            return '<button class="btn btn-dark btn-sm">'+ data +'</button>'
            break;
        case '생산':
            return '<button class="btn btn-warning btn-sm">'+ data +'</button>'
            break;
        case '폐기':
            return '<button class="btn btn-danger btn-sm">'+ data +'</button>'
            break;
        case '판매':
            return '<button class="btn btn-primary btn-sm ">'+ data +'</button>'
            break;
    }
}

$(document).on('click', "#releaseEgg tbody tr", function()
{
    let data = releaseTable.row($(this)).data();
    manualReleaseModal(data);
});

function manualReleaseModal(data)
{
    console.log(data);
    $("#id_type").val("생산").change();
    $("#id_productCode").val(data['egg_code']);
    $("#id_in_ymd").val(data['egg_in_ymd']);
    $("#id_fakeYmd").val("");
    $("#id_locationSale").val(null).trigger('change');
    $("#id_in_locatoin").val(data['egg_in_locationCode']);
    $('#id_count').val("").attr("max",data['totalCount']);
    $('#id_price').val("");
    $('#id_memo').val("");
    $("#Modal").modal();
}
function editButtonClick(data)
{
    console.log(data);
    $('#modify_id_count').val(data['count']).removeAttr( "min" );
    $('#modify_id_price').val(data['price']);
    $('#modify_id_memo').val(data['memo']);
    $('.codeName').text(data['codeName']);
    $("#eggModifyModal").modal();
}

function deleteButtonClick(data)
{
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

function pdfButtonClick(data)
{
    console.log(data);
    let ymd = data['ymd'];
    let locationCode = data['locationCode'];
    let moneyMark = $("#moneyMark").is(":checked");
    window.open('/eggs/pdf?ymd=' + ymd + '&locationCode=' + locationCode + "&moneyMark=" + moneyMark, '_blank');
}


$( "#id_type" ).change(function() {
    var type = $(this).val();
    if(type == '판매')
    {
        setSaleStyle();
    }
    else
    {
        setNormalStyle();
    }
});

function setNormalStyle()
{
    $("#id_locationSale").val(null).trigger('change');
    $("#id_locationSale").parent().hide("slow");
    $("#releaseLocation").hide("slow");

    $("#releasePrice").hide("slow");
    $("#id_price").parent().hide("slow");
    $("#id_price").val(null);
}

function setSaleStyle()
{
    $("#id_locationSale").parent().show("slow");
    $("#releaseLocation").show("slow");

    $("#releasePrice").show("slow");
    $("#id_price").parent().show("slow");
}

$('.deleteAndEdit').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();
    let url = '/api/eggs/'+id;

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


$('#manualRelease').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    console.log($this);
    let type = $this.find('#id_type').val();
    let fakeYmd = set_yyyymmdd($this.find('#id_fakeYmd').val());
    $this.find('#id_ymd').val(fakeYmd);
    let location = $this.find('#id_locationSale').val();
    let count = parseInt($this.find('#id_count').val());
    let price = parseInt($this.find('#id_price').val());
    let memo = parseInt($this.find('#id_memo').val());
    let data = $this.serialize();

    $.ajax({
    url: '/eggs/release',
    type: 'post',
    data: data,
    }).done(function(data) {
        alert('수정완료');
        $(".everyModal").modal('hide');
        $('#stepTwo .datatable').DataTable().search($("input[type='search']").val()).draw();
    }).fail(function() { alert('수정 에러 전산실로 문의바랍니다.'); });
});

$('#calculateAmount').click( function () {
    let datas = table.rows('.selected').data();
    if(datas.length > 0)
    {
        var Flag = true;
        let typeCheck = datas[0]['type'];
        var pk = datas[0]['id'];
        $.each(datas, function( index, data ) {
            if(index > 0)
            {
                if(typeCheck == data["type"])
                {
                    pk = pk + "," + data['id'];
                }
                else {  Flag = false; }
            }
        });
    }
    else
    {
        alert('대상을 선택해주세요');
        return false;
    }

    if(Flag)
    {
        $("#pks").val(pk);
        $("#calculateAmountModal").modal();
    }
    else
    {
        alert('동일한 구분만 선택하세요.');
        return false;
    }
});

$('#calculateAmountForm').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let amount = $this.find('#id_amount').val();
    let data = $this.serialize();

    if(amount > 0)
    {
        $.ajax({
        url: 'eggs/calculateAmount',
        type: 'post',
        data: data,
        }).done(function(data) {
            alert('수정완료');
            $('.datatable').DataTable().search($("input[type='search']").val()).draw();
            $(".everyModal").modal('hide');
        }).fail(function() {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    }
    else
    {
        alert("출고중량을 0보다 크게 입력해주세요");
        return false;
    }
});

$('#pricePerEa').click( function () {
    let start_date = $('#start_date').val();
    let end_date = $('#end_date').val();
    let answer = confirm(`${start_date} ~ ${end_date} 생산단가작업을 실행 하시겠습니까?`);
    if (answer) {
        start_date = set_yyyymmdd(start_date);
        end_date = set_yyyymmdd(end_date);
        let data = `start_date=${start_date}&end_date=${end_date}`;
        $.ajax({
        url: 'eggs/pricePerEa',
        type: 'post',
        data: data,
        }).done(function(data) {
            alert('완료');
            $('.datatable').DataTable().search($("input[type='search']").val()).draw();
            $(".everyModal").modal('hide');
        }).fail(function() {
            alert('해당 기간 내 입고 원란의 구매금액을 확인해주세요.');
        });
    }
});

