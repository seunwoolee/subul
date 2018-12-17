 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
 fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let checkBoxFilter = $('.type_filter input:checkbox:checked').map(function(){ return $(this).val(); }).get().join(',');
    $('.datatable').DataTable().destroy();
    table = $('.datatable').DataTable({
        "language": {searchPlaceholder: "제품명, 메모"},
        "processing": true,
        "serverSide": true,
        "order" : [[5, "asc"]],
        "ajax": {
            "url": "/api/product/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date, checkBoxFilter:checkBoxFilter
            }
        },
        "columns": [
            {"data": "id"},
            {"data": "master_id", "visible": false},
            {"data": "type", "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "code"},
            {"data": "codeName"},
            {"data": "ymd"},
            {"data": "amount" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "count" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "rawTank_amount", "render":function(data, type, row, meta){return setTankAmountStyle(data);}},
            {"data": "pastTank_amount","render": function(data, type, row, meta){return setTankAmountStyle(data);}},
            {"data": "loss_insert" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "loss_openEgg" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "loss_clean" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "loss_fill" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "memo", "render": function(data, type, row, meta){return setMemoStyle(data);}},
            {"data": null, "render": function(data, type, row, meta){return setDataTableActionButton();}}
        ],

        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'pageLength',
                        className:'btn btn-light',
                        text : '<i class="fas fa-list-ol fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'colvis',
                        className:'btn btn-light',
                        text : '<i class="far fa-eye fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'copy',
                        className:'btn btn-light',
                        text : '<i class="fas fa-copy fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    },
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]],
        drawCallback: function(settings) {
                $('[data-toggle="tooltip"]').tooltip();
            }
    });
 }

function setTypeButton(data)
{
    switch(data)
    {
        case '할란':
            return '<button class="btn btn-danger btn-sm">'+ data +'</button>'
            break;
        case '할란사용':
            return '<button class="btn btn-warning btn-sm">'+ data +'</button>'
            break;
        case '공정품투입':
            return '<button class="btn btn-success btn-sm">'+ data +'</button>'
            break;
        case '공정품발생':
            return '<button class="btn btn-primary btn-sm ">'+ data +'</button>'
            break;
        case '제품생산':
            return '<button class="btn btn-dark btn-sm">'+ data +'</button>'
            break;
    }
}

function setTankAmountStyle(data)
{
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

function setMemoStyle(data)
{
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

var AMOUNT_KG = {};
function editButtonClick(data)
{
    if(data['type'] == "제품생산")
    {
        window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"]};
        console.log(window.AMOUNT_KG);
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

function deleteButtonClick(data)
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
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
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

$(".amount").focusout(function(){ setAutoCountValue($(this)); });
$(".count").focusout(function(){ setAutoAmountValue($(this)); });
