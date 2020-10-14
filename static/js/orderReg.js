$(function () {
    $('#id_form-0-product').find('option').remove(); // HACK 장고 select is_valid 특성상 choices를 보내줘야함
    // 보기 지저분하니 Front 단에서 삭제
    $('input[type=date]').val(end_day);
});

SEQ = 2;

function cloneMore(selector, prefix) {
    $(selector).find('.location').select2("destroy");
    let previousLocationValue = $(selector).find('.location').val();
    let newElement = $(selector).clone(true);
    let no = newElement.find('.no');
    let total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    newElement.find(':input').each(function () {
        setNewElementInputInfo($(this), total, previousLocationValue);
    });
    total++;
    no.html(SEQ).css("background-color", "");
    SEQ++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    let conditionRow = $('.forms-row:not(:last)');
    minusConditionRow(conditionRow, 'normal');
    $('.django-select2').djangoSelect2();
    return false;
}

function setNewElementInputInfo($this, total, previousLocationValue) {
    var name = $this.attr('name');
    if (name) {
        name = name.replace('-' + (total - 1) + '-', '-' + total + '-');
        var id = 'id_' + name;

        if (name.indexOf("type") >= 0 || name.indexOf("set") >= 0 || name.indexOf("specialTag") >= 0) {  // 타입,일반/특인,세트는 판매로 고정한다(사용자 편의)
            $this.attr({'name': name, 'id': id});
        } else if (name.indexOf("location") >= 0) // 그 전의 location을 그대로 가져온다(사용자 편의)
        {
            $this.attr({'name': name, 'id': id}).val(previousLocationValue).trigger('change');
        } else if (name.indexOf("product") >= 0) // 이전의 제품 option 값 지우기
        {
            $this.attr({'name': name, 'id': id}).find('option').remove();
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

function cloneSetMore(selector, prefix) {
    parentTR = $(selector);
    PRODUCT = parentTR.find('.product').val();
    COUNT = parentTR.find('.count').val();

    if (COUNT > 0) {
        url = '/api/OrderSetProductMatch/' + PRODUCT;
        $.ajax({
            url: url,
            type: 'get',
            async: false,
            data: data,
        }).done(function (data) {
            parentTR.find('.location').select2("destroy");
            var newElement = parentTR.clone(true);

            for (i = 0; i < data.length; i++) {
                var newElement = newElement.clone(true);
                var no = newElement.find('.no');
                var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
                newElement.find(':input:not(:button)').each(function () {
                    setPackageElementInputInfo(parentTR, $(this), data, total);
                });
                total++;
                $('#id_' + prefix + '-TOTAL_FORMS').val(total);
                $(selector).after(newElement);
                newElement.find('button').each(function () {
                    let conditionRow = $(this);
                    (i == data.length - 1) ? plusConditionRow(conditionRow) : minusConditionRow(conditionRow, 'package');
                });
                no.html(SEQ).css("background-color", "yellow");
                SEQ++;
            }

            let parentTR_temp = parentTR;
            for (i = 0; i < data.length - 1; i++) {
                parentTR_temp = parentTR_temp.next('tr');
                setReadOnly(parentTR_temp);
            }

            $('.django-select2').djangoSelect2();
            deleteForm('form', parentTR.find(':button'));
        }).fail(function () {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    } else {
        alert("수량을 입력하세요");
        return false;
    }
}

function setPackageElementInputInfo(parentTR, $this, data, total) {
    PRODUCT = parentTR.find('.product').val();
    COUNT = parentTR.find('.count').val();
    SET = parentTR.find('.set').val();
    TYPE = parentTR.find('.type').val();
    LOCATION = parentTR.find('.location').val();

    var name = $this.attr('name');
    if (name) {
        name = name.replace('-' + (total - 1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        if (name.indexOf("set") >= 0) {
            $this.attr({'name': name, 'id': id});
        } else if (name.indexOf("amount_kg") >= 0) {
            $this.attr({'name': name, 'id': id}).val(data[i]['amount_kg']);
        } else if (name.indexOf("type") >= 0) {
            $this.attr({'name': name, 'id': id}).val(TYPE);
        } else if (name.indexOf("location") >= 0) {
            $this.attr({'name': name, 'id': id}).val(LOCATION);
        } else if (name.indexOf("product") >= 0) //제품명 option 낑가넣기
        {
            let option = $("<option value=" + data[i]["code"] + " selected>" + data[i]["codeName"] + "</option>");
            $this.attr({'name': name, 'id': id}).find('option').remove();
            $this.append(option);
        } else if (name.indexOf("amount") >= 0) {
            $this.attr({
                'name': name,
                'id': id
            }).val(parseFloat(data[i]["amount"] * COUNT).toFixed(2)).removeAttr('readonly');
        } else if (name.indexOf("count") >= 0) {
            $this.attr({'name': name, 'id': id}).val(data[i]["count"] * COUNT);
        } else if (name.indexOf("price") >= 0) {
            let price = data[i]["price"];
            if (OLAP_SHOPPINGMALL === LOCATION && $("#employeePrice input:checkbox").is(":checked")) {
                price = data[i]["price"] * 0.7;
            }
            $this.attr({'name': name, 'id': id}).val(price).removeAttr('readonly');
        } else if (name.indexOf("package") >= 0) {
            $this.attr({'name': name, 'id': id}).val(PRODUCT);
        } else if (name.indexOf("specialTag") >= 0) {
            $this.attr({'name': name, 'id': id}).removeAttr('disabled');
        } else // hidden fields
        {
            $this.attr({'name': name, 'id': id});
        }
    }
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
    let location = parentTR.find('.location').val();
    let price = parentTR.find('.price');
    let packages = parentTR.find('input[name*="package"]').val();

    if ($('form')[0].checkValidity()) {
        if (!packages && OLAP_SHOPPINGMALL === location && $("#employeePrice input:checkbox").is(":checked")) {
            price.val(Math.round(price.val() * 0.7));
        }
        cloneMore('.forms-row:last', 'form');
        setReadOnly($(this).parents('tr'));
        calculatePriceCount();
    } else {
        alert('정보를 모두 알맞게 넣어주세요(빨간색->녹색)');
    }
    return false;
});

$(document).on('click', '.add-form-set', function (e) { // 패키지 상품 버튼
    e.preventDefault();
    cloneSetMore('.forms-row:last', 'form');
    calculatePriceCount();
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
$(".location").change(function () {

    OLAP_SHOPPINGMALL = '00416';
    parentTR = $(this).parents('tr');
    data = parentTR.find('.location').val();
    set = parentTR.find('.set').val();
    type = parentTR.find('.type').val();
    product = parentTR.find('.product');
    price = parentTR.find('.price');
    specialTag = parentTR.find('.specialTag').val();
    (set == '일반') ? url = '/api/OrderProductUnitPrice/' + data : url = '/api/OrderSetProductCode/' + data;

    if (OLAP_SHOPPINGMALL == data) {
        $('#employeePrice').show();
    } else {
        $("#employeePrice input:checkbox").prop("checked", false);
        $('#employeePrice').hide();
    }

    if (data) {
        $.ajax({
            url: url,
            type: 'get',
            data: data,
        }).done(function (data) {
            window.PRODUCTINFO = [];
            data.sort((a, b) => {
                return (a.codeName < b.codeName) ? -1 : (a.codeName === b.codeName) ? 0 : 1;
            })
            product.empty();
            data.forEach(function (element, i) {
                var option = $("<option value=" + element["code"] + " >" + element["codeName"] + "</option>");
                product.append(option);

                if (i === 0 && set == '일반') {
                    window.AMOUNT_KG = {"parentTR": parentTR, "AMOUNT_KG": element["amount_kg"]};
                    if (type == '판매') {
                        (specialTag == "") ? price.val(element["price"]) : price.val(element["specialPrice"]);
                    } else {
                        price.val(0);
                    }
                }

                if (set == '일반') {
                    var temp = {
                        "code": element["code"],
                        "amount_kg": element["amount_kg"],
                        "price": element["price"],
                        "specialPrice": element["specialPrice"]
                    };
                    PRODUCTINFO.push(temp);
                }
            })
        }).fail(function () {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    } else {
        return false;
    }
});

$(".product").change(function () {
    parentTR = $(this).parents('tr');
    data = parentTR.find('.product').val();
    type = parentTR.find('.type').val();
    price = parentTR.find('.price');
    amount = parentTR.find('.amount');
    specialTag = parentTR.find('.specialTag').val();

    PRODUCTINFO.forEach(function (element) {

        if (data == element["code"]) {
            window.AMOUNT_KG = {"parentTR": parentTR, "AMOUNT_KG": element["amount_kg"]};
            window.AMOUNT_KG['AMOUNT_KG'] = element["amount_kg"];

            if (type == '판매') {
                (specialTag == "") ? price.val(element["price"]) : price.val(element["specialPrice"]);
            } else {
                price.val(0);
            }

            amount.focusout();

        }
    })
});

$(".type").change(function () {
    parentTR = $(this).parents('tr');
    type = parentTR.find('.type').val();
    price = parentTR.find('.price');
    if (type != '판매') {
        price.val(0);
    } else {
        parentTR.find('.location').change();
    }
});

$(".specialTag").change(function () {
    parentTR = $(this).parents('tr');
    data = parentTR.find('.product').val();
    specialTag = parentTR.find('.specialTag').val();
    set = parentTR.find('.set').val();
    PRODUCTINFO.forEach(function (element) {
        if (data == element["code"] && AMOUNT_KG['parentTR'][0] == parentTR[0]) {
            window.AMOUNT_KG = {"parentTR": parentTR, "AMOUNT_KG": element["amount_kg"]};
            window.AMOUNT_KG['AMOUNT_KG'] = element["amount_kg"];
            if (specialTag == "") {
                price.val(element["price"]);
            } else {
                price.val(element["specialPrice"]);
            }
        }
    })
});

$(".set").change(function () {
    parentTR = $(this).parents('tr');
    set = parentTR.find('.set').val();
    (set == '패키지') ? makeSetStyle(parentTR) : makeNormalStyle(parentTR);
    parentTR.find('.location').change();
});

$(".amount").focusout(function () {
    set = parentTR.find('.set').val();
    if (set == '일반' && AMOUNT_KG['parentTR'][0] == parentTR[0]) {
        setAutoCountValue($(this));
    }
});

$(".count").focusout(function () {
    set = parentTR.find('.set').val();
    if (set == '일반' && AMOUNT_KG['parentTR'][0] == parentTR[0]) {
        setAutoAmountValue($(this));
    }
});

$("#submitButton").click(function (e) {
    e.preventDefault();

    if ($('.add-form-set').length !== 0) {
        alert('세트상품을 확인해주세요 검정색 버튼 클릭 필요!');
        return false;
    }

    if ($('form')[0].checkValidity()) {
        let dayOfWeek = getDayOfWeek($('input[type=date]').val());
        if (confirm(`주문일자가 ${$('input[type=date]').val()} ${dayOfWeek}요일이 맞습니까?`)) {
            ymd = set_yyyymmdd($('input[type=date]').val());
            $("input[type=hidden][id*='ymd']").each(function (i, element) {
                $(element).val(ymd);
            });
            $("input:disabled").prop('disabled', false);
            $('.django-select2').prop("disabled", false);
            $("form").submit();
        } else {
            return false;
        }
    }

});

$('.custom-file-input').on('change', function () {
    const fileName = $(this).val().split("\\").pop();
    $(this).siblings('.custom-file-label').html(fileName);
});

$('#excelSaveButton').click(function () {
    const url = 'order/excelUpload';
    const files = $('#excelUploadButton').prop('files');
    const formData = new FormData();
    formData.append("excelFile", files[0]);
    $.ajax({
        url: url,
        type: 'post',
        data: formData,
        contentType: false,
        processData: false,
    }).done(function () {
        alert('성공');
    }).fail(function (error) {
        const invalidLocations =  error.responseJSON[0];
        const invalidProducts = error.responseJSON[1];
        let errorMessage = '';

        for (let i = 0; i < invalidLocations.length; i++) {
            errorMessage += `[행 : ${invalidLocations[i]}] 거래처 이름을 확인하세요 \n`;
        }

        for (let i = 0; i < invalidProducts.length; i++) {
            errorMessage += `[행 : ${invalidProducts[i]}] 제품 이름을 확인하세요 \n`;
        }

        alert(errorMessage);
    })
});

function makeSetStyle(parentTR) {
    parentTR.find('.price').attr('readonly', 'readonly').val("");
    parentTR.find('.amount').attr('readonly', 'readonly').val("");
    parentTR.find('.count').val("");
    parentTR.find('.product').find('option').remove();
    actonButton = parentTR.find('.input-group-append > button');
    actonButton.attr('class', 'btn btn-dark add-form-set');
    actonButton.html('<i class="nav-icon icon-star"></i>');
    parentTR.find('.specialTag').prop('disabled', true).val("일반");
}

function makeNormalStyle(parentTR) {
    parentTR.find('.price').removeAttr('readonly');
    parentTR.find('.amount').removeAttr('readonly');
    parentTR.find('.count').val("");
    parentTR.find('.product').find('option').remove();
    actonButton = parentTR.find('.input-group-append > button');
    actonButton.attr('class', 'btn btn-success add-form-row');
    actonButton.html('+');
    parentTR.find('.specialTag').prop('disabled', false);
}

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

