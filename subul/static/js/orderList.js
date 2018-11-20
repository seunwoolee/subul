 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
    table = $('.datatable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": { start_date:start_date, end_date:end_date }
        },
         "createdRow": function( row, data, dataIndex ) {
            $( row ).find('td:eq(0)').attr('data-title','ID');
            $( row ).find('td:eq(1)').attr('data-title','구분');
            $( row ).find('td:eq(2)').attr('data-title','특인');
            $( row ).find('td:eq(3)').attr('data-title','주문일');
            $( row ).find('td:eq(4)').attr('data-title','거래처명');
            $( row ).find('td:eq(5)').attr('data-title','품명');
            $( row ).find('td:eq(6)').attr('data-title','양(KG)');
            $( row ).find('td:eq(7)').attr('data-title','개수(EA)');
            $( row ).find('td:eq(8)').attr('data-title','단가');
            $( row ).find('td:eq(9)').attr('data-title','금액');
            $( row ).find('td:eq(10)').attr('data-title','메모');
            $( row ).find('td:eq(11)').attr('data-title','세트명');
            $( row ).find('td:eq(12)').attr('data-title','Actions');
         },
        "columns": [
            {"data": "id"},
            {"data": "type", "render" : function(data, type, row, meta){return setTypeButton(data);}},
            {"data": "specialTag", "render" : function(data, type, row, meta){return setSpecialTagButton(data);}},
            {"data": "ymd"},
            {"data": "orderLocationName"},
            {"data": "codeName"},
            {"data": "amount"},
            {"data": "count"},
            {"data": "price"},
            {"data": "totalPrice"},
            {"data": "memo"},
            {"data": "setProduct"},
            {"data": null, "render": function(data, type, row, meta){return setDataTableActionButton();}}
        ],
        dom: 'Bfrtip',
        buttons: ['pageLength', 'colvis','copy', 'excel', 'pdf', 'print'],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]]
    });
 }

function setTypeButton(data)
{
    switch(data)
    {
        case '판매':
            return '<button class="btn btn-dark btn-sm">'+ data +'</button>'
            break;
        case '샘플':
            return '<button class="btn btn-warning btn-sm">'+ data +'</button>'
            break;
        case '증정':
            return '<button class="btn btn-success btn-sm">'+ data +'</button>'
            break;
        case '자손':
            return '<button class="btn btn-primary btn-sm ">'+ data +'</button>'
            break;
        case '생산요청':
            return '<button class="btn btn-danger btn-sm">'+ data +'</button>'
            break;
    }
}

$('#search').click(function(){ // TODO serach 3갠데 고민한번 해봐야함/...
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

function editButtonClick(data)
{
    $('#amount').val(data['amount']);
    $('#count').val(data['count']);
    $('#price').val(data['price']);
    $('.memo').val(data['memo']);
    $('.modal_title').text('EDIT');
    $('.codeName').text(data['codeName']);
    $("#orderModal").modal();
}

function deleteButtonClick(data)
{
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

$('form').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let data = $this.serialize();
    url = '/api/order/'+id;

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


