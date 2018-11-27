/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.1.1): datatables.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */



SEQ = 2;
function cloneMore(selector, prefix) {

    $(selector).find('select').select2("destroy");
    var newElement = $(selector).clone(true);
    var no = newElement.find('.no');

    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name')
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    total++;
    no.html(SEQ);
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

AMOUNT_KG = {};
$( ".product" ).change(function() {
    parentTR = $(this).parents('tr');
    data = parentTR.find('.product').val();
    url = '/api/productCodes/'+data;

    $.ajax({
    url: url,
    type: 'get',
    data: data,
    }).done(function(data) {
        window.AMOUNT_KG = {"parentTR" : parentTR, "AMOUNT_KG" : data["amount_kg"]};
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });

});

$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.forms-row:last', 'form');
    return false;
});

$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});

//$("form").submit(function(){
//    e.preventDefault();
//    $('input[type=date]').attr("pattern","[0-9]{4}-[0-9]{2}-[0-9]{2}")
//    ymd = set_yyyymmdd($('input[type=date]').val());
//    $('input[type=date]').val(ymd);
////    $("form").submit();
//})


$(".amount").focusout(function(){ if(AMOUNT_KG['parentTR'][0] == parentTR[0]) { setAutoCountValue($(this)); }});
$(".count").focusout(function(){ if(AMOUNT_KG['parentTR'][0] == parentTR[0]) { setAutoAmountValue($(this)); }});

