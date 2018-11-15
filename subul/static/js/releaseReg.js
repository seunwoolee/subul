/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.1.1): datatables.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

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



var date = new Date();
var days = 7;
var plusSevenDate = new Date(date.getTime() + (days * 24 * 60 * 60 * 1000));
var start_day = date.yyyymmdd();
var end_day = plusSevenDate.yyyymmdd();

 $('.input-daterange').datepicker({
  todayBtn:'linked',
  format: "yyyymmdd",
  autoclose: true
 });


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
            "data": {
                start_date:start_date, end_date:end_date
            }
        },
        "columns": [
            {

                "data": "id"
            },
            {
                "data": "type",
                "render" : function(data, type, row, meta){
                    if(data == '판매')
                    {
                        return '<button class="btn btn-dark btn-sm">'+ data +'</button>'
                    }
                    else if(data == '샘플')
                    {
                        return '<button class="btn btn-warning btn-sm">'+ data +'</button>'
                    }
                    else if(data == '증정')
                    {
                        return '<button class="btn btn-success btn-sm">'+ data +'</button>'
                    }
                    else if(data == '자손')
                    {
                        return '<button class="btn btn-primary btn-sm ">'+ data +'</button>'
                    }
                    else if(data == '생산요청')
                    {
                        return '<button class="btn btn-danger btn-sm">'+ data +'</button>'
                    }
                }
            },
            {"data": "ymd"},
            {"data": "orderLocationName"},
            {"data": "codeName"},
            {"data": "amount"},
            {"data": "count"},
            {"data": "memo"},
//            {"data": "totalPrice"},
//            {"data": "memo"},
//            {"data": "setProduct"},
//            {
//                "data": null,
//                "defaultContent": '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="fa fa-trash-o"></i></button>' +
//                                    '<button class="btn btn-info btn-sm MODIFY" href="#"><i class="fa fa-edit"></i></button>'
//            }
        ],
        dom: 'Bfrtip',
        buttons: ['pageLength', 'colvis','copy', 'excel', 'pdf', 'print'],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
}

$('#search').click(function(){
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
$(document).on('click', ".datatable tbody tr", function() {
    let data = table.row($(this)).data();
    console.log(data);
    totalAmount = data['totalAmount'];
    totalCount = data['totalCount'];
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
    $('#datepicker').val("");
    $("#Modal").modal();
});

var ORDER_AMOUNT = 0.0;
var ORDER_COUNT = 0;
var STORE_TOTAL_AMOUNT=0.0;
var STORE_TOTAL_COUNT=0;
var BOOL = true;
$(document).on('click', "#orderDatatable tbody tr", function() {
    window.ORDER_AMOUNT = 0.0;
    window.ORDER_COUNT = 0;
    window.STORE_TOTAL_AMOUNT=0.0;
    window.STORE_TOTAL_COUNT=0;
    window.BOOL = true;

    var data = orderTable.row($(this)).data();
    window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"]};
    console.log('ORDER 데이터 ↓');
    console.log(data);
    data['storedLocation'] = $('#id_storedLocation').val();
    var storedLocationName = $('#id_storedLocation option:selected').text();
    var releaseInfoOne = `  <span>보관장소 : ${storedLocationName}(${data['storedLocation']}),
                            납품일 : ${data['ymd']},
                            거래처명 : ${data['orderLocationName']}</span>`;

    var releaseInfoTwo = `  <span>제품명 : ${data['codeName']},
                            주문량 : ${data['amount']}KG,
                            주문수량 : ${data['count']}EA </span>`;

    $.ajax({
    url: '/api/productAdmin/',
    type: 'get',
    data: data,
    }).done(function(rows) {
        console.log(rows);
        $('.releaseInfoOne span').remove();
        $('.releaseInfoTwo span').remove();
        $('#orderModal tbody tr').remove();
        $('.releaseInfoOne').append(releaseInfoOne);
        $('.releaseInfoTwo').append(releaseInfoTwo);
        window.ORDER_AMOUNT = data['amount']; // 총 주문량
        window.ORDER_COUNT = data['count'];

        $(rows).each(function(i, row){ // 총 재고수량을 파악한다
            window.STORE_TOTAL_AMOUNT += row['totalAmount'];
            window.STORE_TOTAL_COUNT += row['totalCount'];
        });

        $(rows).each(function(i, row){
            calculateData = {};
            calculateData['totalAmount'] = row['totalAmount'];
            calculateData['totalCount'] = row['totalCount'];
            var TR = `<tr>
                         <td>
                            <input type="hidden" name="productId">
                            <input type="hidden" name="productYmd">
                            <input type="hidden" name="productCode">
                            <input type="hidden" name="storedLocationCode">
                            <input type="hidden" name="location">
                            <input type="hidden" name="type">
                            <input type="hidden" name="ymd">
                            <input type="hidden" name="price">
                            <input type="hidden" name="releaseOrder">
                            <input type="hidden" name="amount_kg">
                            <input type="hidden" name="setProductCode">
                            <input type="hidden" name="memo">
                            ${data['codeName']}
                         </td>
                         <td>${row['productYmd']}</td>
                         <td>${row['totalAmount']}</td>
                         <td>${row['totalCount']}</td>
                         <td><input type="number" name="amount" class="form-control amount"></td>
                         <td><input type="number" name="count" class="form-control count"></td>
                    </tr>`;
            $TR = $('#orderModal tbody').append(TR);
            $TR = $TR.find('tr:last');
            insertInputValue($TR, row, data);
            if( window.ORDER_AMOUNT >= window.STORE_TOTAL_AMOUNT) // 총 주문량이 더 많기 때문에 총 재고량을 각각 val에 박아준다
            {
                $TR.find('.amount').val(row['totalAmount']);
                $TR.find('.count').val(row['totalCount']);
            }
            else if(BOOL)// 재고량이 더많을때
            {
                calculateReleaseAmount($TR,calculateData);
            }
        });

        $("#orderModal").modal();
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

function calculateReleaseAmount($TR, DATA)
{
    if( window.ORDER_AMOUNT >= DATA['totalAmount']) //주문량이 더크니 -하고 내꺼박고
    {
        $TR.find('.amount').val(DATA['totalAmount']);
        $TR.find('.count').val(DATA['totalCount']);
        window.ORDER_AMOUNT -= DATA['totalAmount'];
        window.ORDER_COUNT -= DATA['totalCount'];
    }
    else // 마침내 드디어 주문량이 더 작아졌다 주문량을 박자
    {
        window.ORDER_AMOUNT = Math.round(window.ORDER_AMOUNT * 100) / 100;
        window.ORDER_COUNT = Math.round(window.ORDER_COUNT * 100) / 100;
        $TR.find('.amount').val(window.ORDER_AMOUNT);
        $TR.find('.count').val(window.ORDER_COUNT);
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
    $TR.find('input[name="ymd"]').val(data['ymd']);
    $TR.find('input[name="price"]').val(data['price']);
    $TR.find('input[name="releaseOrder"]').val(data['id']);
    $TR.find('input[name="amount_kg"]').val(data['amount_kg']);
    $TR.find('input[name="setProductCode"]').val(data['setProductCode']);
    $TR.find('input[name="memo"]').val("");
}

$(function () {
  $("#datepicker").datepicker({
        autoclose: true,
        todayHighlight: true,
        format:'yyyymmdd'
  });
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$(document).on('focusout', ".amount", function() {
    parentTR = $(this).parents('tr');
    amount = $(this).val();
    amount = Math.round(amount * 100) / 100;
    count = amount / window.AMOUNT_KG['AMOUNT_KG'];
    parentTR.find('.count').val(count);
});

$(document).on('focusout', ".count", function() {
    parentTR = $(this).parents('tr');
    count = $(this).val();
    count = Math.round(count * 100) / 100;
    amount = count * window.AMOUNT_KG['AMOUNT_KG'];
    parentTR.find('.amount').val(amount);
});

$('#manualRelease').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    count = $this.find('#id_count').val();
    amount = $this.find('#id_amount').val();
    let data = $this.serialize();
    console.log(data);
    url = '/release/';

    if(totalCount >= count)
    {
        $.ajax({
        url: url,
        type: 'post',
        data: data,
        }).done(function(data) {
            alert('수정완료');
            $(".everyModal").modal('hide');
            $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        }).fail(function() {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    }
    else
    {
        alert('수량을 확인해 주세요');
    }
});

$('#orderRelease').on('submit', function (e)
{
    e.preventDefault();
    len = $("#orderRelease tbody tr").length;
    url = '/release/';
    for(var i=0; i<len; i++)
    {
        var amount = $("#orderRelease tbody tr:eq("+i+")").find('input[name="amount"]').val();
        var count = $("#orderRelease tbody tr:eq("+i+")").find('input[name="count"]').val();
        if( amount > 0 && count > 0)
        {
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
        }
        else
        {
            alert('출하량이 0보다 커야합니다');
        }
    }
});


