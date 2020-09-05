$('#search').click(function () {

    if (typeof LOCATION_MANAGER != "undefined") {
        LOCATION_MANAGER = false;
    }

    let start_date = $('#start_date').val();
    let end_date = $('#end_date').val();
    if (start_date !== '' && end_date !== '') {
        fetch_data(start_date, end_date);
    } else {
        alert("날짜를 모두 입력해주세요");
    }
});

$('.datatable tbody, #eggDatatable tbody').on('click', 'button', function () {

    if ($(this).parents('table').attr('id') === 'eggOrderDatatable') {
        let data = eggOrderTable.row($(this).parents('tr')).data();
        let class_name = $(this).attr('class');
        if (class_name === 'btn btn-info btn-sm MODIFY') {
            eggOrderEditButtonClick(data);
        } else if (class_name === 'btn btn-danger btn-sm REMOVE') {
            eggOrderDeleteButtonClick(data);
        }
        id = data['id'];
        return;
    }

    let data = table.row($(this).parents('tr')).data();
    let class_name = $(this).attr('class');
    if (class_name === 'btn btn-info btn-sm MODIFY') {
        editButtonClick(data);
    } else if (class_name === 'btn btn-danger btn-sm REMOVE') {
        deleteButtonClick(data);
    } else if (class_name === 'btn btn-warning btn-sm PDF') {
        pdfButtonClick(data);
    } else if (class_name === 'btn btn-default btn-sm PDF') {
        pdfMoveButtonClick(data);
    } else if (class_name === 'btn btn-success btn-sm RECALL') {
        recallButtonClick(data);
    }
    id = data['id'];
});
