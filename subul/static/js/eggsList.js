fetch_data();
function fetch_data()
{
    table = $('.datatable').DataTable({
        "language": {
        "lengthMenu": "_MENU_ 페이지당 개수",
        "zeroRecords": "결과 없음",
        "info": "",
        "infoEmpty": "No records available",
        "infoFiltered": "(검색된결과 from _MAX_ total records)"
        },
         "createdRow": function( row, data, dataIndex ) {
            $( row ).find('td:eq(0)').attr('data-title','거래처명');
            $( row ).find('td:eq(1)').attr('data-title','제품명');
            $( row ).find('td:eq(2)').attr('data-title','생산일');
            $( row ).find('td:eq(3)').attr('data-title','재고수량');
         },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/eggs/",
            "type": "GET"
        },
        "columns": [
            {"data": "egg_in_locationCodeName"},
            {"data": "egg_codeName"},
            {"data": "egg_in_ymd"},
            {"data": "totalCount" , "render": $.fn.dataTable.render.number( ',')},
        ],
        dom: 'Bfrtip',
    });
}

 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
egg_fetch_data(start_day, end_day);
function egg_fetch_data(start_date='', end_date='')
{
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let releaseTypeFilter = $('.type_filter #releaseType_List select').val();
    let productTypeFilter = $('.type_filter #releaseProduct_List select').val();
    let locatoinTypeFilter = $('.type_filter #releaseLocation_List select').val();

    eggTable = $('#eggDatatable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/eggsList/",
            "type": "GET",
            "data": {
                start_date:start_date,
                end_date:end_date,
                releaseTypeFilter:releaseTypeFilter,
                productTypeFilter:productTypeFilter,
                locatoinTypeFilter:locatoinTypeFilter
                }
        },
        "responsive" : true,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: 3 },
            { responsivePriority: 3, targets: -1, orderable: false },
            { orderable: false, targets: 9 },
            { orderable: false, targets: 10 },
            { orderable: false, targets: 11 }
        ],
        "columns": [
            {"data": "id"},
            {"data": "type", "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "in_ymd"},
            {"data": "codeName"},
            {"data": "in_locationCodeName"},
            {"data": "locationCodeName"},
            {"data": "ymd"},
            {"data": "count" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "amount" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "in_price" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "out_price" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "pricePerEa" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "memo"},
            {"data": null, "render": function(data, type, row, meta){return setDataTableActionButton();}}
        ],
        dom: 'Bfrtip',
        buttons: ['pageLength', 'colvis','copy', 'excel', 'pdf', 'print'],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
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

$('#search').click(function(){ //TODO 합칠수있으면 합치자
    var start_date = $('#start_date').val();
    var end_date = $('#end_date').val();
    if(start_date != '' && end_date !='')
    {
       $('#eggDatatable').DataTable().destroy();
       egg_fetch_data(start_date, end_date);
    }
    else
    {
       alert("날짜를 모두 입력해주세요");
    }
});

$(document).on('click', ".datatable tbody tr", function()
{
    let data = table.row($(this)).data();
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

var ORDER_AMOUNT = 0.0;
var ORDER_COUNT = 0;
var STORE_TOTAL_AMOUNT=0.0;
var STORE_TOTAL_COUNT=0;
var BOOL = true;
$(document).on('click', "#orderDatatable tbody tr", function() {
    resetOrderData();
    var data = orderTable.row($(this)).data();
    console.log('ORDER 데이터 ↓');
    console.log(data);
    data['storedLocation'] = $('#id_storedLocation').val();
    window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"]};
    var storedLocationName = $('#id_storedLocation option:selected').text();
    var releaseInfoOne = setReleaseInfoOne(storedLocationName, data);
    var releaseInfoTwo = setReleaseInfoTwo(data);

    $.ajax({
    url: '/api/productAdmin/',
    type: 'get',
    data: data,
    }).done(function(rows) {
        console.log(rows);
        changeReleaseInfo(releaseInfoOne, releaseInfoTwo);
        setOrderAmount(data);
        setStoredTotalAmount(rows);

        $(rows).each(function(i, row){
            var TR = setOrderReleaseTrModal(data,row);
            $TR = $('#orderModal tbody').append(TR);
            $TR = $TR.find('tr:last');
            insertInputValue($TR, row, data);
            if( window.ORDER_AMOUNT >= window.STORE_TOTAL_AMOUNT) // 총 주문량이 더 많기 때문에 총 재고량을 각각 val에 박아준다
            {
                $TR.find('.amount').val(row['totalAmount']);
                $TR.find('.count').val(row['totalCount']);
                $TR.find('.datepicker').val(data['ymd']);
            }
            else if(BOOL)// 재고량이 더많을때
            {
                calculateData = {};
                calculateData['totalAmount'] = row['totalAmount'];
                calculateData['ymd'] = data['ymd'];
                calculateData['totalCount'] = row['totalCount'];
                calculateReleaseAmount($TR,calculateData);
            }
        });
        setDatePicker();
        $("#orderModal").modal();
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

$('#orderRelease').on('submit', function (e)
{
    e.preventDefault();
    len = $("#orderRelease tbody tr").length;
    url = '/release/';
    for(var i=0; i<len; i++)
    {
            var data = $("#orderRelease tbody tr:eq("+i+") :input").serialize();
            var request = $.ajax({
            url: url,
            type: 'post',
            data: data,
            }).done(function(data) {
                    $(".everyModal").modal('hide');
                    $('#orderDatatable').DataTable().search($("input[type='search']").val()).draw();
            }).fail(function() {
                alert('수정 에러 전산실로 문의바랍니다.');
            });
    }
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

    console.log(data);

    $.ajax({
    url: '/eggs/release',
    type: 'post',
    data: data,
    }).done(function(data) {
        alert('수정완료');
        $(".everyModal").modal('hide');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
    }).fail(function() { alert('수정 에러 전산실로 문의바랍니다.'); });

});


