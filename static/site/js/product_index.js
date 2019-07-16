$(function () {

    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });

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

setInterval(getTableList, 10000);


$('.open-button').click(function () { $('#createForm').css('display', 'block'); });

$('.close-button').click(function () { $('#createForm').css('display', 'none'); });

AMOUNT_KG = {};
$("#id_productCode").change(function () {

    if ($(this).val()) {
        let pk = $(this).val();

        $.ajax({
            url: '/api/productCodeByPk/' + pk,
            type: 'get',
        }).done(function (data) {
            window.AMOUNT_KG = {"AMOUNT_KG": data["amount_kg"]};
            console.log(window.AMOUNT_KG);
        }).fail(function () {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    }
});

$('.has-spinner').click(function () {
    let btn = $(this);
    let form = btn.closest("form");

    if (form[0].checkValidity()) {
        $(btn).buttonLoader('start');
        setTimeout(function () {
            $(btn).buttonLoader('stop');
        }, 1000);
        form.submit();
    }
});

$("#createForm form").submit(function (e) {
    e.preventDefault();

    let data = $(this).serialize();
    let type = 'post';
    let url = '/product/order';

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('완료');
        $('#id_ymd').val('');
        $('#id_count').val('');
        $('#id_amount').val('');
        $('#id_memo').val('');
        $('.django-select2').val('');
        $('.django-select2').trigger('change');

        getTableList();

    }).fail(function () {
        alert('에러발생! 전산팀으로 문의 바랍니다.');
    });
});

function getTableList() {
    $.ajax({
        url: '/labor/product',
        type: 'get',
    }).done(function (data) {
        $("div.table").html(data.list);
    }).fail(function () {
        alert('에러발생: 브라우저 및 PC를 리부팅하세요');
    });
}

function setAutoCountValue($this) {
    if ($this.val().length > 0) {
        parentTR = $this.parents('tr');
        amount = $this.val();
        count = amount / window.AMOUNT_KG['AMOUNT_KG'];
        count = Math.round(count * 100) / 100;
        parentTR.find('.count').val(count);
        parentTR.find('.amount_kg').val(window.AMOUNT_KG['AMOUNT_KG']);
    }
}

function setAutoAmountValue($this) {
    if ($this.val().length > 0) {
        parentTR = $this.parents('tr');
        count = $this.val();
        amount = count * window.AMOUNT_KG['AMOUNT_KG'];
        amount = Math.round(amount * 100) / 100;
        parentTR.find('.amount').val(amount);
        parentTR.find('.amount_kg').val(window.AMOUNT_KG['AMOUNT_KG']);
    }
}

$(".amount").focusout(function () { setAutoCountValue($(this)); });
$(".count").focusout(function () { setAutoAmountValue($(this)); });

$("#id_ymd").datepicker({
    autoclose: true,
    todayHighlight: true,
    format: 'yyyymmdd'
});
