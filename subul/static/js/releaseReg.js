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
            $( row ).find('td:eq(0)').attr('data-title','제품');
            $( row ).find('td:eq(1)').attr('data-title','생산일');
            $( row ).find('td:eq(2)').attr('data-title','위치');
            $( row ).find('td:eq(3)').attr('data-title','재고량(KG)');
            $( row ).find('td:eq(4)').attr('data-title','재고수량(EA)');
         },
        "paging": false,
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/productAdmin/",
            "type": "GET"
        },
        "columns": [
            {"data": "productCodeName"},
            {"data": "productYmd"},
            {"data": "storedLocationCodeName"},
            {"data": "totalAmount"},
            {"data": "totalCount"},
        ],
        dom: 'Bfrtip',
    });
}

 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
order_fetch_data(start_day, end_day);
function order_fetch_data(start_date='', end_date='')
{
    orderTable = $('#orderDatatable').DataTable({
        "paging": false,
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": { start_date:start_date, end_date:end_date }
        },
         "createdRow": function( row, data, dataIndex ) {
            $( row ).find('td:eq(0)').attr('data-title','ID');
            $( row ).find('td:eq(1)').attr('data-title','타입');
            $( row ).find('td:eq(2)').attr('data-title','특인');
            $( row ).find('td:eq(3)').attr('data-title','주문일');
            $( row ).find('td:eq(4)').attr('data-title','거래처');
            $( row ).find('td:eq(5)').attr('data-title','제품명');
            $( row ).find('td:eq(6)').attr('data-title','주문량(KG)');
            $( row ).find('td:eq(7)').attr('data-title','주문수량(EA)');
            $( row ).find('td:eq(8)').attr('data-title','메모');
         },
        "columns": [
            {"data": "id"},
            {"data": "type", "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "specialTag", "render" : function(data, type, row, meta){return setSpecialTagButton(data);}},
            {"data": "ymd"},
            {"data": "orderLocationName"},
            {"data": "codeName"},
            {"data": "amount"},
            {"data": "count"},
            {"data": "memo"},
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
    }
}

$('#search').click(function(){ //TODO 합칠수있으면 합치자
    var start_date = $('#start_date').val();
    var end_date = $('#end_date').val();
    if(start_date != '' && end_date !='')
    {
       $('#orderDatatable').DataTable().destroy();
       order_fetch_data(start_date, end_date);
    }
    else
    {
       alert("날짜를 모두 입력해주세요");
    }
});

var AMOUNT_KG = {};
var totalAmount = 0;
var totalCount = 0;
$(document).on('click', ".datatable tbody tr", function()
{
    let data = table.row($(this)).data();
    setNormalLocationStyle();
    manualReleaseModal(data);
});

function manualReleaseModal(data)
{
    window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"]};
    $('#id_productId').val(data['productId']);
    $('#id_productYmd').val(data['productYmd']);
    $('#id_productCode').val(data['productCode']);
    $('#id_storedLocationCode').val(data['storedLocationCode']);
    $('#id_amount').val("");
    $('#id_price').val("");
    $('#id_memo').val("");
    $('#id_count').val("");
    $('#id_releaseOrder').val(0);
    $('#id_amount_kg').val(data['amount_kg']);
    $('#id_totalCount').val(data['totalCount']);
    $('#datepicker').val("");
    $("#Modal").modal();
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

function resetOrderData()
{
    window.ORDER_AMOUNT = 0.0;
    window.ORDER_COUNT = 0;
    window.STORE_TOTAL_AMOUNT=0.0;
    window.STORE_TOTAL_COUNT=0;
    window.BOOL = true;
}

function setReleaseInfoOne(storedLocationName, data)
{
    var releaseInfoOne = `  <span>보관장소 : ${storedLocationName}(${data['storedLocation']}),
                            납품일 : ${data['ymd']},
                            거래처명 : ${data['orderLocationName']}</span>`;
    return releaseInfoOne;
}

function setReleaseInfoTwo(data)
{
    var releaseInfoTwo = `  <span>제품명 : ${data['codeName']},
                            주문량 : ${data['amount']}KG,
                            주문수량 : ${data['count']}EA </span>`;
    return releaseInfoTwo;
}

function changeReleaseInfo(releaseInfoOne, releaseInfoTwo)
{
    $('.releaseInfoOne span').remove();
    $('.releaseInfoTwo span').remove();
    $('#orderModal tbody tr').remove();
    $('.releaseInfoOne').append(releaseInfoOne);
    $('.releaseInfoTwo').append(releaseInfoTwo);
}

function setOrderAmount(data)
{
    window.ORDER_AMOUNT = data['amount']; // 총 주문량
    window.ORDER_COUNT = data['count'];
}

function setStoredTotalAmount(rows)
{
    $(rows).each(function(i, row){ // 총 재고수량을 파악한다
        window.STORE_TOTAL_AMOUNT += row['totalAmount'];
        window.STORE_TOTAL_COUNT += row['totalCount'];
    });
}


function calculateReleaseAmount($TR, DATA)
{
    if( window.ORDER_AMOUNT >= DATA['totalAmount']) //주문량이 더크니 -하고 내꺼박고
    {
        $TR.find('.amount').val(DATA['totalAmount']);
        $TR.find('.count').val(DATA['totalCount']);
        $TR.find('.datepicker').val(DATA['ymd']);
        window.ORDER_AMOUNT -= DATA['totalAmount'];
        window.ORDER_COUNT -= DATA['totalCount'];
    }
    else // 마침내 드디어 주문량이 더 작아졌다 주문량을 박자
    {
        window.ORDER_AMOUNT = Math.round(window.ORDER_AMOUNT * 100) / 100;
        window.ORDER_COUNT = Math.round(window.ORDER_COUNT * 100) / 100;
        $TR.find('.amount').val(window.ORDER_AMOUNT);
        $TR.find('.count').val(window.ORDER_COUNT);
        $TR.find('.datepicker').val(DATA['ymd']);
        window.BOOL = false; // 이제 내밑으론 안타도된다! 주문량이 이젠 없으니
    }
}

function insertInputValue($TR, row, data)
{
    $TR.find('input[name="productId"]').val(row['productId']);
    $TR.find('input[name="productYmd"]').val(row['productYmd']);
    $TR.find('input[name="productCode"]').val(row['productCode']);
    $TR.find('input[name="storedLocationCode"]').val(row['storedLocationCode']);
    $TR.find('input[name="location"]').val(data['orderLocationCode']);
    $TR.find('input[name="type"]').val(data['type']);
    $TR.find('input[name="price"]').val(data['price']);
    $TR.find('input[name="releaseOrder"]').val(data['id']);
    $TR.find('input[name="amount_kg"]').val(data['amount_kg']);
    $TR.find('input[name="setProductCode"]').val(data['setProductCode']);
    $TR.find('input[name="memo"]').val("");
    $TR.find('input[name="specialTag"]').val(data["specialTag"]);
}

$(document).on('focusout', ".amount", function() { setAutoCountValue($(this));});
$(document).on('focusout', ".count", function() { setAutoAmountValue($(this));});

$('#manualRelease').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    var count = parseInt($this.find('#id_count').val());
    var type = $this.find('#id_type').val();
    var totalCount = parseInt($this.find('#id_totalCount').val());
    var storedLocationCode = $this.find('#id_storedLocationCode').val();
    var locationCode = $this.find('#id_location').val();
    let data = $this.serialize();
    var url = ((type == "미출고품" || type == "재고조정") ? '/release/adjustment' : '/release/');

    if(type == "이동")
    {
        if(totalCount >= count && storedLocationCode !== locationCode && count > 0)
        {
            manualReleaseAjax(url,data);
        }
        else { alert('장소를 확인해주세요'); }
    }
    else if(type == "미출고품" || type == "재고조정")
    {
        manualReleaseAjax(url,data);
    }
    else
    {
        if(totalCount >= count && count > 0)
        {
            manualReleaseAjax(url,data);
        }
        else { alert('수량을 확인해주세요'); }
    }
});

$('#orderRelease').on('submit', function (e)
{
    e.preventDefault();
    len = $("#orderRelease tbody tr").length;
    url = '/release/';
    for(var i=0; i<len; i++)
    {
//        var amount = $("#orderRelease tbody tr:eq("+i+")").find('input[name="amount"]').val();
//        var count = $("#orderRelease tbody tr:eq("+i+")").find('input[name="count"]').val();
//        if( amount > 0 && count > 0)
//        {
            var data = $("#orderRelease tbody tr:eq("+i+") :input").serialize();
            $.ajax({
            url: url,
            type: 'post',
            data: data,
            }).done(function(data) {
//                if(lastCount == count) # TODO 시간남을떄!
//                {
//                    alert('출고 등록 완료');
                    $(".everyModal").modal('hide');
                    $('#orderDatatable').DataTable().search($("input[type='search']").val()).draw();
            }).fail(function() {
                alert('수정 에러 전산실로 문의바랍니다.');
            });
//        }
//        else
//        {
//            alert('출하량이 0보다 커야합니다');
//        }
    }
});

function setDatePicker()
{
    $(".datepicker").datepicker({
        autoclose: true,
        todayHighlight: true,
        format:'yyyymmdd'
    });
}

function setOrderReleaseTrModal(data, row)
{
    var TR = `<tr>
                 <td data-title="제품명">
                    <input type="hidden" name="productId">
                    <input type="hidden" name="productYmd">
                    <input type="hidden" name="productCode">
                    <input type="hidden" name="storedLocationCode">
                    <input type="hidden" name="location">
                    <input type="hidden" name="type">
                    <input type="hidden" name="ymd" class="datepicker">
                    <input type="hidden" name="price">
                    <input type="hidden" name="releaseOrder">
                    <input type="hidden" name="amount_kg">
                    <input type="hidden" name="setProductCode">
                    <input type="hidden" name="memo">
                    <input type="hidden" name="specialTag">
                    ${data['codeName']}
                 </td>
                 <td data-title="생산일">${row['productYmd']}</td>
                 <td data-title="재고량(KG)">${row['totalAmount']}</td>
                 <td data-title="재고수량(EA)">${row['totalCount']}</td>
                 <td data-title="출하량(KG)"><input type="float" name="amount" class="form-control amount"></td>
                 <td data-title="출하수량(EA)"><input type="number" name="count" class="form-control count"></td>
                 <td data-title="출고일자"><input type="text" name="ymd" class="form-control datepicker"></td>
            </tr>`;
    return TR;
}

$( "#id_type" ).change(function() {
    var type = $(this).val();
    if(type == '이동')
    {
        setMoveLocationStyle();
    }
    else if(type == "미출고품" || type == "재고조정")
    {
        setAdjustmentStyle();
    }
    else
    {
        setNormalLocationStyle();
    }
});

function setMoveLocationStyle()
{
    $("#manualReleaseLocation").text("이동장소");
    $("#id_location").parent().show("slow");
    $("#manualReleaseLocation").show("slow");
    $("#manualReleaseYmd").text("이동일자");
    $("#manualReleasePrice").hide("slow");
    $("#id_price").parent().hide("slow");
    $("#id_price").val(0);
    $("#manualReleaseMemo").hide("slow");
    $("#id_memo").parent().hide("slow");
}

function setNormalLocationStyle()
{
    var type = $("#id_type").val();
    if(type=="이동"){$("#id_type option[value='판매']").prop('selected','true');}

    $("#id_location").parent().show("slow");
    $("#manualReleaseLocation").text("판매처");
    $("#manualReleaseLocation").show("slow");

    $("#manualReleaseYmd").text("출고일자");
    $("#manualReleaseYmd").show("slow");

    $("#manualReleasePrice").show("slow");
    $("#id_price").parent().show("slow");
    $("#id_price").val("");

    $("#manualReleaseMemo").show("slow");
    $("#id_memo").parent().show("slow");
}

function setAdjustmentStyle()
{
    $("#id_location").parent().hide("slow");
    $("#manualReleaseLocation").hide("slow");

    $("#manualReleasePrice").hide("slow");
    $("#id_price").parent().hide("slow");
    $("#id_price").val(0);

    $("#id_amount").removeAttr("min");
    $("#id_count").removeAttr("min");
}

function manualReleaseAjax(url, data)
{
    $.ajax({
    url: url,
    type: 'post',
    data: data,
    }).done(function(data) {
        alert('수정완료');
        $(".everyModal").modal('hide');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
    }).fail(function() { alert('수정 에러 전산실로 문의바랍니다.'); });
}
