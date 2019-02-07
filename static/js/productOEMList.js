 $('#start_date').val(start_day);
 $('#end_date').val(end_day);
 fetch_data(start_day, end_day);
 function fetch_data(start_date='', end_date='')
 {
    start_date = set_yyyymmdd(start_date);
    end_date = set_yyyymmdd(end_date);
    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
    	"footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;
            let numberFormatWithDot = $.fn.dataTable.render.number( ',', '.', 2).display;
            let numberFormat = $.fn.dataTable.render.number( ',').display;

            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };


            let pageTotal_count = api
                .column( 7, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_purchaseSupplyPrice = api
                .column( 8, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_purchaseVat = api
                .column( 9, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            let pageTotal_totalPrice = api
                .column( 10, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 7 ).footer() ).html( numberFormat(pageTotal_count) + '(EA)' );
            $( api.column( 8 ).footer() ).html( numberFormat(pageTotal_purchaseSupplyPrice) );
            $( api.column( 9 ).footer() ).html( numberFormat(pageTotal_purchaseVat) );
            $( api.column( 10 ).footer() ).html( numberFormat(pageTotal_totalPrice) );
        },
        "responsive": true,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: -1, orderable: false },
            { responsivePriority: 3, targets: 2 },
            { targets: 7, className: "dt-body-right" },
            { targets: 8, className: "dt-body-right" },
            { targets: 9, className: "dt-body-right" },
            { targets: 10, className: "dt-body-right" },
        ],
        "language": {searchPlaceholder: "거래처명, 제품명, 메모"},
        "processing": true,
        "serverSide": true,
        "order" : [[5, "asc"]],
        "ajax": {
            "url": "/api/productOEM/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date
            }
        },
        "columns": [
            {"data": "id"},
            {"data": "purchaseYmd"},
            {"data": "ymd"},
            {"data": "locationCode_code"},
            {"data": "purchaseLocationName"},
            {"data": "code"},
            {"data": "codeName"},
            {"data": "count" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "purchaseSupplyPrice" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "purchaseVat" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "totalPrice" , "render": $.fn.dataTable.render.number( ',')},
            {"data": "memo"},
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
        rowCallback: function(row, data, index){
             $('td:eq(1)', row).html( set_yyyy_mm_dd(data.purchaseYmd) );
             $('td:eq(2)', row).html( set_yyyy_mm_dd(data.ymd) );
        }
    });


 }

function editButtonClick(data)
{
    $('#modify_id_purchaseSupplyPrice').val(data['purchaseSupplyPrice']);
    $('#modify_id_purchaseVat').val(data['purchaseVat']);
    $('#modify_id_memo').val(data['memo']);
    $('.codeName').text(data['codeName']);
    $("#modifyModal").modal();
}

function deleteButtonClick(data)
{
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
}

$('.deleteAndEdit').on('submit', function (e)
{
    e.preventDefault();
    $this = $(this);
    let type = $this.find('.ajaxUrlType').val();
    let data = $this.serialize();
    let url = '/api/productOEM/'+id;

    $.ajax({
    url: url,
    type: type,
    data: data,
    }).done(function(data) {
        alert('완료');
        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
        $(".everyModal").modal('hide');
    }).fail(function() {
        alert('수정 에러 전산실로 문의바랍니다.');
    });
});

//$('form').on('submit', function (e)
//{
//    e.preventDefault();
//    $this = $(this);
//    let data = $this.serialize();
//    let type = $this.find('.ajaxUrlType').val();
//    url = setAjaxUrl($this);
//
//    $.ajax({
//    url: url,
//    type: type,
//    data: data,
//    }).done(function(data) {
//        alert('완료');
//        $('.datatable').DataTable().search($("input[type='search']").val()).draw();
//        $(".everyModal").modal('hide');
//    }).fail(function() {
//        alert('수정 에러 전산실로 문의바랍니다.');
//    });
//});