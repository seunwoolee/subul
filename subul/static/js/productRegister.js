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
});

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }


var t = $('.datatable').DataTable({
        "language": {
            "lengthMenu": "_MENU_ 페이지당 개수",
            "zeroRecords": "결과 없음",
            "info": "page _PAGE_ of _PAGES_",
            "infoEmpty": "No records available",
            "infoFiltered": "(검색된결과 from _MAX_ total records)"
        }
});

	
hotkeys('BackSpace,f5', function(event, handler) {
  // Prevent the default refresh event under WINDOWS system
  event.preventDefault();
});

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
    }).done(function(data) { // data는  code, codeName, amount_kg를 담고있다
        window.AMOUNT_KG = {"parentTR" : parentTR, "AMOUNT_KG" : data["amount_kg"]};
//        window.AMOUNT_KG = data["amount_kg"];
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


$(".amount").focusout(function(){
    parentTR = $(this).parents('tr');
    if(AMOUNT_KG['parentTR'][0] == parentTR[0])
    {
        amount = $(this).val();
        count = amount / window.AMOUNT_KG['AMOUNT_KG'];
        parentTR.find('.count').val(count);
    }
});


$(".count").focusout(function(){
    parentTR = $(this).parents('tr');
    if(AMOUNT_KG['parentTR'][0] == parentTR[0])
    {
        count = $(this).val();
        amount = count * window.AMOUNT_KG['AMOUNT_KG'];
        parentTR.find('.amount').val(amount);
    }
});


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




// $('#select2-3').select2({
  // theme: 'bootstrap',
  // placeholder: 'Your Favorite Football Team',
  // allowClear: true
// });
//# sourceMappingURL=datatables.js.map