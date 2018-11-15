/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.1.1): datatables.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------

 */

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
            {"data": "id"},
            {"data": "master_id", "visible": false},
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
            {"data": "code"},
            {"data": "codeName"},
            {"data": "ymd"},
            {"data": "amount"},
            {"data": "count"},
            {
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
            {"data": "loss_insert"},
            {"data": "loss_openEgg"},
            {"data": "loss_clean"},
            {"data": "loss_fill"},
            {
                "data": "memo",
                "render": function(data, type, row, meta){
                        if(data)
                        {
                            return `<span style="font-size : 1rem;">
                                        <i class="fas fa-file-alt" data-toggle="tooltip" data-placement="top"
                                         title=${data}>
                                         </i>
                                     </span>`
                        }
                        else
                        {
                            return ""
                        }
                }
            },
            {
                "data": null,
                "defaultContent": '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="fa fa-trash-o"></i></button>' +
                                    '<button class="btn btn-info btn-sm MODIFY" href="#"><i class="fa fa-edit"></i></button>'
            }
        ],
        dom: 'Bfrtip',
        buttons: ['pageLength', 'colvis','copy', 'excel', 'pdf', 'print'],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]],
        drawCallback: function(settings) {
                $('[data-toggle="tooltip"]').tooltip();
            }
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
       alert("날짜를 모두 입력해주세요");
  }
 });


$('.datatable tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info btn-sm MODIFY')  // EDIT button
    {
        if(data['type'] == "제품생산")
        {
            $('#amount').val(data['amount']);
            $('#count').val(data['count']);
            $('.memo').val(data['memo']);
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
    else if(class_name == 'btn btn-danger btn-sm REMOVE')// DELETE button
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

    $.ajax({
    url: url,
    type: 'patch',
    data: data,
    }).done(function(data) {
        alert('수정완료');
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

function makeAjaxUrl($this)
{
    let productType = $this.find("input[name='productType']").val();
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

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})