$(function () {

    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });

    // HACK 백앤드에서 ModelForm chocie를 먹여도 삭제가안됨
    $("select[name='type'] option[value='전란']").remove();
    $("select[name='type'] option[value='난백난황']").remove();

    $("#id_ymd").val(ymd);
    $("#id_code").val(codes);
    $("#id_codeName").val(codeNames);
    $("#id_productCode").val(productCode);
    $("#id_amount_kg").val(amount_kg);
    $("#id_pk").val(pk);

    $("#futureStockForm .count").val(future_stock_count);
    $("#futureStockForm .amount").val(future_stock_amount);

    $("#pastStockForm .count").val(past_stock_count);
    $("#pastStockForm .amount").val(past_stock_amount);

    $("#createPackingStockModal #id_type").val('재고');

    if(!past_stock_amount){
        $("#createPackingStockModal select[name='stock_type'] option[value='전주재고']").remove();
    } else {
        $("#createPackingStockModal input[name='amount']").attr('max',past_stock_amount);
    }

    if(!future_stock_count){
        $("#createPackingStockModal select[name='stock_type'] option[value='차주재고']").remove();
    } else {
        $("#createPackingStockModal input[name='amount']").attr('max',future_stock_amount);
    }

});

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

$(document).on('change', '#createPackingStockModal select[name="stock_type"]', function () {
    let stock_type = $(this).val();

    if(stock_type === '전주재고'){
         $("#createPackingStockModal input[name='amount']").attr('max',past_stock_amount);
    }

    if(stock_type === '차주재고'){
         $("#createPackingStockModal input[name='amount']").attr('max',future_stock_amount);
    }
});

$(document).on('submit', 'form', function (e)
{
    e.preventDefault();

    let data = $(this).serialize();
    let type = $(this).find('.ajaxUrlType').val();
    let url = $(this).attr('action');

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('완료');
        location.reload();
    }).fail(function (xhr, status, error) {
        if(xhr.status === 412){
            alert('이미 생성된 재고가 있습니다.');
        } else {
            alert('에러발생! 전산팀으로 문의 바랍니다.');
        }
    });
});

$(document).on('click', '.MODIFY', function () {
    let parentDiv = $(this).closest('div');
    let id = parentDiv.attr('data-id');
    let url = parentDiv.attr('data-url');

    let boxCount = parentDiv.attr('data-boxCount');
    let eaCount = parentDiv.attr('data-eaCount');

    $('#id_boxCount').val(boxCount);
    $('#id_eaCount').val(eaCount);

    $("#modifyModal form").attr('action', url);

    $("#modifyModal").modal();
});

$(document).on('click', '.ADDSTOCK', function () {
    let parentDiv = $(this).closest('div');
    let id = parentDiv.attr('data-id');
    $("#createPackingStockModal #id_origin_pk").val(id);
    $("#createPackingStockModal").modal();

});

$(document).on('click', '.REMOVE', function () {
    let parentDiv = $(this).closest('div');
    let url = parentDiv.attr('data-url');

    $('#modal_title').text('DELETE');
    $("#confirm form").attr('action', url);
    $("#confirm").modal();
});

$(document).on('click', '.stock-button', function () {
    let parentDiv = $(this).closest('div');
    let id = parentDiv.attr('data-id');
    $('#confirm form').attr('action', '/api/productOrderPacking/' + id);

    $("#stockModal").modal();
});

$(document).on('click', '.RELEASE-STOCK', function (e) {
    let parentDiv = $(this).closest('div');
    let id = parentDiv.attr('data-id');
    let url = '/api/productOrderReleaseStock/' + id;
    let stockName = parentDiv.find('h3').text();

    $.ajax({
        url: url,
        type: 'POST',
        data: {"orderLocationCodeName": stockName},
    }).done(function (data) {
        alert('완료');
        location.reload();
    }).fail(function (xhr, status, error) {
        alert('에러발생! 전산팀으로 문의 바랍니다.');
    });

});

$(document).on('focusout', '.amount', function () {
    setAutoCountValue($(this));
});

$(document).on('focusout', '.count', function () {
    setAutoAmountValue($(this));
});

