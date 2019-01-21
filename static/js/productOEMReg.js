/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.1.1): datatables.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

SEQ = 2;
function cloneMore(selector, prefix) {

    $(selector).find('.location').select2("destroy");
    $(selector).find('.product').select2("destroy");
    var newElement = $(selector).clone(true);
    var no = newElement.find('.no');
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    newElement.find(':input').each(function() { setNewElementInputInfo($(this), total); });
    total++;
    no.html(SEQ).css("background-color", "");
    SEQ++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.forms-row:not(:last)');
    minusConditionRow(conditionRow, 'normal');
    $('.django-select2').djangoSelect2();
    return false;
}

function setNewElementInputInfo($this, total)
{
    var name = $this.attr('name');
    if(name) {
        name = name.replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $this.attr({'name': name, 'id': id}).val('').removeAttr('checked');
    }
}

function minusConditionRow(conditionRow, type)
{
    if(type == "normal"){ conditionRow = conditionRow.find('.btn.add-form-row'); }
    conditionRow.removeClass('btn-success').removeClass('btn-dark').addClass('btn-danger')
    .removeClass('add-form-row').removeClass('add-form-set').addClass('remove-form-row')
    .html('-');
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

$(document).on('click', '.remove-form-row', function(e){ // 삭제 - 버튼
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});


$("form").submit(function(){
    ymd = set_yyyymmdd($('input[type=date]').val());
    if(ymd)
    {
        $("input[type=hidden][id*='ymd']").each(function (i, element){
            $(element).val(ymd);
        });
        $("form").submit();
    }
})

$(".fakeYmd").focusout(function(){
    let fakeYmd = $(this).val();
    if(fakeYmd.length == 10)
    {
        let ymd = set_yyyymmdd(fakeYmd);
        parentTR = $(this).parents('tr');
        parentTR.find('.ymd').val(ymd);
    }
});

$(".fakePurchaseYmd").focusout(function(){
    let fakeYmd = $(this).val();
    if(fakeYmd.length == 10)
    {
        let ymd = set_yyyymmdd(fakeYmd);
        parentTR = $(this).parents('tr');
        parentTR.find('.purchaseYmd').val(ymd);
    }
});
