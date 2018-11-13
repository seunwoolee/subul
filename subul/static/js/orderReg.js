/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.1.1): datatables.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

 $(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $('#id_form-0-product').find('option').remove(); // HACK 장고 select is_valid 특성상 choices를 보내줘야함
                                                        // 보기 지저분하니 Front 단에서 삭제
});

SEQ = 2;
function cloneMore(selector, prefix) {

    $(selector).find('.location').select2("destroy");
    var newElement = $(selector).clone(true);
    var no = newElement.find('.no');
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    newElement.find(':input').each(function() {
        var name = $(this).attr('name')
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;

            if(name.indexOf("type") >= 0 || name.indexOf("set") >= 0) // 타입,세트는 판매로 고정한다(사용자 편의)
            {
                $(this).attr({'name': name, 'id': id});
            }
            else if(name.indexOf("product") >= 0) // 이전의 제품 option 값 지우기
            {
                $(this).attr({'name': name, 'id': id}).find('option').remove();
            }
            else
            {
                $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
            }
        }
    });
    total++;
    no.html(SEQ).css("background-color", "");
    SEQ++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.forms-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('-');

    $('.django-select2').djangoSelect2();
    return false;
}

function cloneSetMore(selector, prefix) {

    parentTR = $(selector);
    PRODUCT = parentTR.find('.product').val();
    COUNT = parentTR.find('.count').val();
    SET = parentTR.find('.set').val();
    TYPE = parentTR.find('.type').val();
    LOCATION = parentTR.find('.location').val();

    if(COUNT > 0)
    {
        url = '/api/OrderSetProductMatch/'+PRODUCT;
        $.ajax({
        url: url,
        type: 'get',
        data: data,
        }).done(function(data) { // data 는  code, codeName, price, count, amount_kg을 담고있다.

            parentTR.find('.location').select2("destroy");
            var newElement = parentTR.clone(true);

            for(i=0;i<data.length;i++)
            {
                var newElement = newElement.clone(true);
                var no = newElement.find('.no');
                var total = $('#id_' + prefix + '-TOTAL_FORMS').val();

                newElement.find(':input:not(:button)').each(function() { // 각각의 input 마다(세로)
                    var name = $(this).attr('name');
                    if(name) {
                        name = name.replace('-' + (total-1) + '-', '-' + total + '-');
                        var id = 'id_' + name;
                        if(name.indexOf("set") >= 0)
                        {
                            $(this).attr({'name': name, 'id': id});
                        }
                        else if(name.indexOf("type") >= 0 )
                        {
                            $(this).attr({'name': name, 'id': id}).val(TYPE);
                        }
                        else if(name.indexOf("location") >= 0)
                        {
                            $(this).attr({'name': name, 'id': id}).val(LOCATION);
                        }
                        else if(name.indexOf("product") >= 0) //제품명 option 낑가넣기
                        {
                            var option = $("<option value="+data[i]["code"]+" selected>"+data[i]["codeName"]+"</option>");
                            $(this).attr({'name': name, 'id': id}).find('option').remove();
                            $(this).append(option);
                        }
                        else if(name.indexOf("amount") >= 0)
                        {
                            $(this).attr({'name': name, 'id': id}).val(data[i]["amount"] * COUNT).removeAttr('readonly');
                        }
                        else if(name.indexOf("count") >= 0)
                        {
                            $(this).attr({'name': name, 'id': id}).val(data[i]["count"] * COUNT);
                        }
                        else if(name.indexOf("price") >= 0)
                        {
                            $(this).attr({'name': name, 'id': id}).val(data[i]["price"]).removeAttr('readonly');
                        }
                        else if(name.indexOf("package") >= 0)
                        {
                            $(this).attr({'name': name, 'id': id}).val(PRODUCT);
                        }
                        else // hidden fields
                        {
                            $(this).attr({'name': name, 'id': id});
                        }
                    }
                });

                total++;
                $('#id_' + prefix + '-TOTAL_FORMS').val(total);
                $(selector).after(newElement);

                 newElement.find('button').each(function() {

                    var conditionRow = $(this);
                    if(i == data.length -1)
                    {
                        conditionRow.removeClass('btn-dark').removeClass('btn-danger')
                                    .addClass('btn-success')
                                    .removeClass('remove-form-row').removeClass('add-form-set')
                                    .addClass('add-form-row').html('+');
                    }
                    else
                    {
                        conditionRow.removeClass('btn-dark').addClass('btn-danger')
                                    .removeClass('add-form-set').addClass('remove-form-row').html('-');
                    }
                 });


                no.html(SEQ).css("background-color", "yellow");
                SEQ++;
            }
            $('.django-select2').djangoSelect2();
            console.log(parentTR.find(':button'));
            deleteForm('form',parentTR.find(':button'));
        }).fail(function() {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    }
    else
    {
        alert("수량을 입력하세요");
        return false;
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
    if (total > 1){
        btn.closest('.forms-row').remove();
        var forms = $('.forms-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0; i<forms.length; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

$(document).on('click', '.add-form-row', function(e){ //일반상품 + 버튼
    e.preventDefault();
    cloneMore('.forms-row:last', 'form');
    return false;
});

$(document).on('click', '.add-form-set', function(e){ // 패키지 상품 버튼
    e.preventDefault();
    cloneSetMore('.forms-row:last', 'form');
    return false;
});

$(document).on('click', '.remove-form-row', function(e){ // 삭제 - 버튼
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});


PRODUCTINFO = [];
AMOUNT_KG = {};
$( ".location" ).change(function() {

    parentTR = $(this).parents('tr');
    data = parentTR.find('.location').val();
    set = parentTR.find('.set').val();
    product = parentTR.find('.product');
    price = parentTR.find('.price');


    if(set == '일반')
    {
        url = '/api/OrderProductUnitPrice/'+data;
    }
    else if(set == '패키지')
    {
        url = '/api/OrderSetProductCode/'+data;
    }

    if(data)
    {
        $.ajax({
        url: url,
        type: 'get',
        data: data,
        }).done(function(data) { // data는  price, code, codeName, amount_kg를 담고있다
            window.PRODUCTINFO = [];
            product.empty();
            data.forEach(function(element, i){
                var option = $("<option value="+element["code"]+" >"+element["codeName"]+"</option>");
                product.append(option);

                if(i === 0 && set == '일반')
                {
                    window.AMOUNT_KG = {"parentTR" : parentTR, "AMOUNT_KG" : element["amount_kg"]};
                    price.val(element["price"]);
                }

                if(set == '일반')
                {
                    var temp = { "code" : element["code"], "price" : element["price"], "amount_kg" : element["amount_kg"]  };
                    PRODUCTINFO.push(temp);
                }
            })
        }).fail(function() {
            alert('수정 에러 전산실로 문의바랍니다.');
        });
    }
    else
    {
        return false;
    }

});


$( ".product" ).change(function() {
    parentTR = $(this).parents('tr');
    data = parentTR.find('.product').val();
    price = parentTR.find('.price');
    PRODUCTINFO.forEach(function(element){
        if(data == element["code"])
        {
            AMOUNT_KG = {"parentTR" : parentTR, "AMOUNT_KG" : element["amount_kg"]};
            price.val(element["price"]);
            window.AMOUNT_KG['AMOUNT_KG'] = element["amount_kg"];
        }

    })
});


$( ".set" ).change(function() {
    parentTR = $(this).parents('tr');
    set = parentTR.find('.set').val();
    if(set == '패키지')
    {
        makeSetStyle(parentTR);
    }
    else
    {
        makeNormalStyle(parentTR);
    }

});


$(".amount").focusout(function(){
    parentTR = $(this).parents('tr');
    set = parentTR.find('.set').val();

    if(set == '일반' && AMOUNT_KG['parentTR'][0] == parentTR[0]) // 자기자신의 TR만 변경하겠금
    {
        amount = $(this).val();
        count = amount / window.AMOUNT_KG['AMOUNT_KG'];
        parentTR.find('.count').val(count);
        parentTR.find('.amount_kg').val(window.AMOUNT_KG['AMOUNT_KG']);

    }
})



$(".count").focusout(function(){ // 자기 TR만 바꿀수 있어야함
    parentTR = $(this).parents('tr');
    set = parentTR.find('.set').val();
    if(set == '일반' && AMOUNT_KG['parentTR'][0] == parentTR[0])
    {
        count = $(this).val();
        amount = count * window.AMOUNT_KG['AMOUNT_KG'];
        amount = Math.round(amount * 100) / 100;
        parentTR.find('.amount').val(amount);
        parentTR.find('.amount_kg').val(window.AMOUNT_KG['AMOUNT_KG']);
    }
})

$("form").submit(function(){
    ymd = $('#datepicker').val();
    if(ymd)
    {
        $("input[type=hidden][id*='ymd']").each(function (i, element){
            $(element).val(ymd);
        });
        $("form").submit();
    }
})


function makeSetStyle(parentTR)
{
    price = parentTR.find('.price').attr('readonly','readonly').val("");
    amount = parentTR.find('.amount').attr('readonly','readonly').val("");
    count = parentTR.find('.count').val("");
    product = parentTR.find('.product').find('option').remove();
    actonButton = parentTR.find('.input-group-append > button');
    actonButton.attr('class','btn btn-dark add-form-set');
    actonButton.html('<i class="nav-icon icon-star"></i>');
}

function makeNormalStyle(parentTR)
{
    price = parentTR.find('.price').removeAttr('readonly');
    amount = parentTR.find('.amount').removeAttr('readonly');
    count = parentTR.find('.count').val("");
    product = parentTR.find('.product').find('option').remove();
    actonButton = parentTR.find('.input-group-append > button');
    actonButton.attr('class','btn btn-success add-form-row');
    actonButton.html('+');
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