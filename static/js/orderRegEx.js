$(function () {
    if (isStaff && EXCOMPANY) {
        alert("주문 가능한 시간대가 아닙니다.");
    }

    $('#id_form-0-product').find('option').remove();
    $('input[type=date]').val(end_day);

    var url = '/api/OrderProductUnitPrice/' + EXCOMPANYCODE
    product = $('.product');
    price = $('.price');

    $.ajax({
        url: url,
        type: 'get',
        data: EXCOMPANYCODE
    }).done(function (data) {
        window.PRODUCTINFO = [];
        product.empty();

        data.sort((a, b) => {
            return (a.codeName < b.codeName) ? -1 : (a.codeName === b.codeName) ? 0 : 1;
        })

        data.forEach(function (element, i) {
            var option = $("<option value=" + element["code"] + " >" + element["codeName"] + "</option>");
            product.append(option);

            if (i === 0) {
                window.AMOUNT_KG = {"code": element["code"], "AMOUNT_KG": element["amount_kg"]};
                price.val(element["price"]);
            }

            var temp = {
                "code": element["code"],
                "amount_kg": element["amount_kg"],
                "price": element["price"],
                "specialPrice": element["specialPrice"]
            };
            PRODUCTINFO.push(temp);
        })
    }).fail(function () {
        console.log('fail');
        alert('수정 에러 전산실로 문의바랍니다.');
    });


});

SEQ = 2;

function cloneMore(selector, prefix) {
    let newElement = $(selector).clone(true);
    let no = newElement.find('.no');
    let total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    newElement.find(':input').each(function () {
        setNewElementInputInfo($(this), total);
    });
    total++;
    no.html(SEQ).css("background-color", "");
    SEQ++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    let conditionRow = $('.forms-row:not(:last)');
    minusConditionRow(conditionRow, 'normal');
    return false;
}

function setNewElementInputInfo($this, total) {
    var name = $this.attr('name');
    if (name) {
        name = name.replace('-' + (total - 1) + '-', '-' + total + '-');
        var id = 'id_' + name;

        if (name.indexOf("type") >= 0 || name.indexOf("set") >= 0 || name.indexOf("specialTag") >= 0) {  // 타입,일반/특인,세트는 판매로 고정한다(사용자 편의)
            $this.attr({'name': name, 'id': id});
        } else {
            $this.attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    }
}

function minusConditionRow(conditionRow, type) {
    if (type == "normal") {
        conditionRow = conditionRow.find('.btn.add-form-row');
    }
    conditionRow.removeClass('btn-success').removeClass('btn-dark').addClass('btn-danger')
        .removeClass('add-form-row').removeClass('add-form-set').addClass('remove-form-row')
        .html('-');
}

function plusConditionRow(conditionRow) {
    conditionRow.removeClass('btn-dark').removeClass('btn-danger')
        .addClass('btn-success')
        .removeClass('remove-form-row').removeClass('add-form-set')
        .addClass('add-form-row').html('+');
}

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1) {
        btn.closest('.forms-row').remove();
        let forms = $('.forms-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (let i = 0; i < forms.length; i++) {
            $(forms.get(i)).find(':input').each(function () {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

$(document).on('click', '.add-form-row', function (e) { //일반상품 + 버튼
    e.preventDefault();
    let OLAP_SHOPPINGMALL = '00416';
    let parentTR = $(this).parents('tr');
    let price = parentTR.find('.price');

    if ($('form')[0].checkValidity()) {
        cloneMore('.forms-row:last', 'form');
        setReadOnly($(this).parents('tr'));
        calculatePriceCount();
    } else {
        alert('정보를 모두 알맞게 넣어주세요(빨간색->녹색)');
    }
    return false;
});


$(document).on('click', '.remove-form-row', function (e) { // 삭제 - 버튼
    e.preventDefault();
    deleteForm('form', $(this));
    calculatePriceCount();
    return false;
});

$(document).on('click', '#deleteLastButton', function (e) {

    if (confirm('마지막 줄을 지우시겠습니까?')) {
        let lastButton = $('.add-form-row');
        e.preventDefault();
        deleteForm('form', lastButton);

        if ($('.add-form-row').length === 0) {
            let lastTR = $('.forms-row:last');
            lastTR.find('.count, .amount, .price, .product').each(function () {
                $(this).attr('disabled', false);
            });
            lastTR.find('.product').attr('readonly', false);
            lastTR.find('.django-select2').prop("disabled", false);
            let selectedLocationCode = lastTR.find('.location').val();
            plusConditionRow(lastTR.find('.remove-form-row'));

            $.ajax({
                url: '/api/orderLocation/',
                type: 'get',
                data: {'code': selectedLocationCode},
            }).done(function (data) {
                for (let i = 0; i < data.length; i++) {
                    let option = new Option(data[i].codeName, data[i].code);
                    lastTR.find('.location').append(option);
                }
            }).fail(function () {
                alert('수정 에러 전산실로 문의바랍니다.');
            });
        }
    }
    return false;
});

PRODUCTINFO = [];
AMOUNT_KG = {};

$(".product").change(function () {
    parentTR = $(this).parents('tr');
    data = parentTR.find('.product').val();
    type = parentTR.find('.type').val();
    price = parentTR.find('.price');
    amount = parentTR.find('.amount');
    specialTag = parentTR.find('.specialTag').val();

    PRODUCTINFO.forEach(function (element) {
        if (data == element["code"]) {
            window.AMOUNT_KG = {"code": element["code"], "AMOUNT_KG": element["amount_kg"]};
            window.AMOUNT_KG['AMOUNT_KG'] = element["amount_kg"];
            price.val(element["price"])
            amount.focusout();

        }
    })
});

$(".amount").focusout(function () {
    setAutoCountValue($(this));
});

$(".count").focusout(function () {
    setAutoAmountValue($(this));
});

$("#submitButton").click(function (e) {
    e.preventDefault();

    if (isStaff && EXCOMPANY) {
        alert('주문 가능한 시간이 아닙니다.');
        return false;
    }

    if ($('form')[0].checkValidity()) {
        let dayOfWeek = getDayOfWeek($('input[type=date]').val());
        if (confirm(`주문일자가 ${$('input[type=date]').val()} ${dayOfWeek}요일이 맞습니까?`)) {
            ymd = set_yyyymmdd($('input[type=date]').val());
            $("input[type=hidden][id*='ymd']").each(function (i, element) {
                debugger;
                $(element).val(ymd);
            });
            $("input:disabled").prop('disabled', false);
            $('.django-select2').prop("disabled", false);
            $("form").submit();
        } else {
            return false;
        }
    } else {
        alert('입력칸을 채워주세요(빨간색 -> 녹색)');
        return false;
    }

});

function setReadOnly($parentTR) {
    $parentTR.find('.count, .amount, .price').each(function () {
        $(this).attr('disabled', 'true');
    });
    $parentTR.find('.product').each(function () {
        $(this).attr('readonly', 'true');
        $(this).find('option').not(':selected').remove()
    });
    $parentTR.find('.location').each(function () {
        $(this).find('option').not(':selected').remove()
    });
    $parentTR.find('.django-select2').each(function () {
        $(this).prop("disabled", true);
    });
}

function calculatePriceCount() {
    let total_amount = 0;
    let total_count = 0;
    let total_price = 0;
    let total = $('.price').length;
    $('.price').each(function (index) {
        if (index < total - 1) {
            let parentTR = $(this).parents('tr');
            let amount = parseFloat(parentTR.find('.amount').val());
            let count = parseInt(parentTR.find('.count').val());
            let price = parseInt($(this).val()) * count;
            total_amount += amount;
            total_count += count;
            total_price += price;
        }
    });

    $('#totalAmount').html(total_amount.toFixed(2));
    $('#totalCount').html(total_count.toLocaleString());
    $('#totalPrice').html(total_price.toLocaleString());
}
