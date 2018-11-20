
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
            {"data": "type", "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "code"},
            {"data": "codeName"},
            {"data": "ymd"},
            {"data": "amount"},
            {"data": "count"},
            {"data": "rawTank_amount", "render":function(data, type, row, meta){return setTankAmountStyle(data);}},
            {"data": "pastTank_amount","render": function(data, type, row, meta){return setTankAmountStyle(data);}},
            {"data": "loss_insert"},
            {"data": "loss_openEgg"},
            {"data": "loss_clean"},
            {"data": "loss_fill"},
            {"data": "memo", "render": function(data, type, row, meta){return setMemoStyle(data);}},
            {"data": null, "render": function(data, type, row, meta){return setDataTableActionButton();}}
        ],
        dom: 'Bfrtip',
        buttons: ['pageLength', 'colvis','copy', 'excel', 'pdf', 'print'],
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

function editButtonClick(data)
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
