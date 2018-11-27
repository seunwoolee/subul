 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    let checkBoxFilter = $('.type_filter input:checkbox:checked').map(function(){ return $(this).val(); })
                                                                      .get().join(',');
    console.log(checkBoxFilter);
    table = $('.datatable').DataTable({
        "language": {searchPlaceholder: "거래처, 제품명, 메모"},
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/order/",
            "type": "GET",
            "data": { start_date:start_date, end_date:end_date, checkBoxFilter:checkBoxFilter }
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
            {"data": "amount" , "render": $.fn.dataTable.render.number( ',', '.', 2)},
            {"data": "count" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "price" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "totalPrice" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "memo"},
            {"data": "setProduct"},
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

//$('#search').click(function(){ // TODO serach 3갠데 고민한번 해봐야함/...
//    var start_date = $('#start_date').val();
//    var end_date = $('#end_date').val();
//    if(start_date != '' && end_date !='')
//    {
//       $('.datatable').DataTable().destroy();
//       fetch_data(start_date, end_date);
//    }
//    else
//    {
//       alert("날짜를 모두 입력해주세요");
//    }
// });

var AMOUNT_KG = {};
function editButtonClick(data)
{
    window.AMOUNT_KG = { "AMOUNT_KG" : data["amount_kg"]};
    $('#id_modifyYmd').val(data['ymd']);
    $('#id_type').val(data['type']);
    $('#id_specialTag').val(data['specialTag']);
    $('#id_amount').val(data['amount']);
    $('#id_count').val(data['count']);
    $('#id_price').val(data['price']);
    $('#id_memo').val(data['memo']);
    $('.modal_title').text('EDIT');
    $('.codeName').text(data['codeName']);
    $("#orderModal").modal();
}

$(".amount").focusout(function(){ setAutoCountValue($(this)); });
$(".count").focusout(function(){ setAutoAmountValue($(this)); });

function deleteButtonClick(data)
{
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

$('form').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();
    url = '/api/order/'+id;

    $.ajax({
    url: url,
    type: type,
    data: data,
    }).done(function(data) {
        alert('수정완료');
//        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});


