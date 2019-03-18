 fetch_data();
 function fetch_data(start_date='', end_date='')
 {
    let type = $('.type_filter #id_type').val();

    $('.datatable').DataTable().destroy();

    table = $('.datatable').DataTable({
        "responsive": true,
        "columnDefs": [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: -1, orderable: false },
        ],
        "language": {searchPlaceholder: "거래처명"},
        "processing": true,
        "serverSide": true,
        "order" : [[0, "asc"]],
        "ajax": {
            "url": "/api/location/",
            "type": "GET",
            "data": {
                start_date:start_date, end_date:end_date, type:type
            }
        },
        "columns": [
            {"data": "id"},
            {"data": "codeName"},
            {"data": "location_owner"},
            {"data": "location_phone"},
            {"data": "location_companyNumber"},
            {"data": "location_address"},
            {"data": "type_string"},
            {"data": "character_string"},
            {"data": "location_manager_string"},
            {"data": null, "render": function(data, type, row, meta){return setDataTableActionButtonOnlyModify();}}
        ],
        dom: 'Bfrtip',
        buttons: [
                    {
                        extend: 'excel',
                        className:'btn btn-light',
                        text : '<i class="far fa-file-excel fa-lg"></i>',
                        init : function(api, node, config){
                            $(node).removeClass('btn-secondary');
                        }
                    }],
        lengthMenu : [[30, 50, -1], [30, 50, "All"]],
    });
 }

function editButtonClick(data)
{
    $('#modifyModal #id_codeName').val(data['codeName']);
    $('#modifyModal #id_location_owner').val(data['location_owner']);
    $('#modifyModal #id_location_address').val(data['location_address']);
    $('#modifyModal #id_location_companyNumber').val(data['location_companyNumber']);
    $('#modifyModal #id_location_phone').val(data['location_phone']);
    $('#modifyModal #id_location_manager').val(data['location_manager']);
    $('.codeName').text(data['codeName']);
    $("#modifyModal").modal();
}

$('#modifyModal form').on('submit', function (e)
{
    e.preventDefault();
    let $this = $(this);
    let data = $this.serialize();
    let type = $this.find('.ajaxUrlType').val();
    let url = '/api/location/'+id;

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