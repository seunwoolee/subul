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



Date.prototype.yyyymmdd = function() {
  var mm = this.getMonth() + 1;
  var dd = this.getDate();

  return [this.getFullYear(),
          (mm>9 ? '' : '0') + mm,
          (dd>9 ? '' : '0') + dd
         ].join('');
};

var date = new Date();
var days = 7;
var plusSevenDate = new Date(date.getTime() + (days * 24 * 60 * 60 * 1000));
var start_day = date.yyyymmdd();
var end_day = plusSevenDate.yyyymmdd();
var table;
 $('.input-daterange').datepicker({
  todayBtn:'linked',
  format: "yyyymmdd",
  autoclose: true
 });


 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
    table = $('.datatable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/product/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date
            }
        },
        "columns": [
            {
                "width" : "5%",
                "data": "id"
            },
            {
                "width" : "5%",
                "data": "master_id"
            },
            {
                "data": "type",
                "render" : function(data, type, row, meta){
                    if(data == '할란')
                    {
                        return '<button class="btn btn-danger btn-sm">'+ data +'</button>'
                    }
                    else if(data == '할란사용')
                    {
                        return '<button class="btn btn-warning btn-sm">'+ data +'</button>'
                    }
                    else if(data == '공정품투입')
                    {
                        return '<button class="btn btn-success btn-sm">'+ data +'</button>'
                    }
                    else if(data == '공정품발생')
                    {
                        return '<button class="btn btn-primary btn-sm ">'+ data +'</button>'
                    }
                    else if(data == '제품생산')
                    {
                        return '<button class="btn btn-dark btn-sm">'+ data +'</button>'
                    }
                }
            },
            {"width" : "2%","data": "code"},
            {"data": "codeName"},
            {"width" : "2%","data": "ymd"},
            {"width" : "2%","data": "amount"},
            {"width" : "2%","data": "count"},
            {
                "width" : "2%",
                "data": "rawTank_amount",
                "render": function(data, type, row, meta){
                    if(data < 0)
                    {
                        return '<span class="text-danger">'+ data +'</span>'
                    }
                    else if(data > 0)
                    {
                        return '<span>'+ data +'</span>'
                    }
                    else
                    {
                        return ""
                    }
                }
            },
            {
                "width" : "2%",
                "data": "pastTank_amount",
                "render": function(data, type, row, meta){
                    if(data < 0)
                    {
                        return '<span class="text-danger">'+ data +'</span>'
                    }
                    else if(data > 0)
                    {
                        return '<span>'+ data +'</span>'
                    }
                    else
                    {
                        return ""
                    }
                }
            },
            {"width" : "2%","data": "loss_insert"},
            {"width" : "2%","data": "loss_openEgg"},
            {"width" : "2%","data": "loss_clean"},
            {"width" : "2%","data": "loss_fill"},
            {"data": "memo"},
            {
                "data": null,
                "defaultContent": '<button class="btn btn-danger btn-sm" href="#"><i class="fa fa-trash-o"></i></button>' +
                                    '<button class="btn btn-info btn-sm" href="#"><i class="fa fa-edit"></i></button>'
            }
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
       $('.datatable').DataTable().destroy();
       fetch_data(start_date, end_date);
  }
  else
  {
       alert("Both Date is Required");
  }
 });


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
    no.html(total);
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

$('.datatable tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    console.log(data);
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info btn-sm')  // EDIT button
    {
        if(data['type'] == "제품생산")
        {
            $('#amount').val(data['amount']);
            $('#count').val(data['count']);
            $('.memo').val(data['memo']);
//            $('.type').val('edit');
            $('.modal_title').text('EDIT');
            $('.codeName').text(data['codeName']);
            $('.productType').val('product');
            $("#productModal").modal();
        }
        else // 할란, 할란사용, 공정품투입, 공정품발생
        {
            if(data['codeName'].indexOf('RAW') != -1)
            {
                tank_amount = data['rawTank_amount'];
                $('#tank_amount').val(tank_amount).attr("name","rawTank_amount");
            }
            else
            {
                tank_amount = data['pastTank_amount'];
                $('#tank_amount').val(tank_amount).attr("name","pastTank_amount");
            }
            $('.productType').val('productEgg');
            $('.memo').val(data['memo']);
            $('.type').val('edit');
            $('.modal_title').text('EDIT');
            $('.codeName').text(data['codeName']);
            $("#productEggModal").modal();
        }
    }
    else // DELETE button
    {
        if(data['type'] == "제품생산")
        {
            $('.productType').val('product');
        }
        else
        {
            $('.productType').val('productEgg');
        }
        $('#modal_title').text('DELETE');
        $("#confirm").modal();
    }

    id = data['id'];

});


$('form').on('submit', function (e)  // EDIT
{
    e.preventDefault();
    $this = $(this);
    let data = $this.serialize();
    url = makeAjaxUrl($this);

    console.log(data);

    $.ajax({
    url: url,
    type: 'patch',
    data: data,
    }).done(function(data) {
        alert('수정완료');
        $(".everyModal").modal('hide');
    //some code going here if success
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

function makeAjaxUrl($this)
{
    let productType = $this.find("input[name='productType']").val();
    console.log(productType);
    if(productType == 'product')
    {
        url = '/api/product/'+id;
    }
    else if(productType == 'productEgg')
    {
        url = '/api/productEgg/'+id;
    }
    return url;
}


//$('#delete').on('click', function (e) {
//    e.preventDefault();
//    alert();
//    $this = $(this);
//    console.log($this);
//    let data = $this.serialize();
//    url = makeAjaxUrl($this);
//    console.log(data);
//
//    $.ajax({
//    url: url,
//    type: 'PUT',
//    data: data,
//    }).done(function(data) {
//        alert('수정완료');
//        $("#productModal").modal('hide');
//    //some code going here if success
//    }).fail(function() {
//        alert('수정 에러 전산실로 문의바랍니다.');
//    });
//});