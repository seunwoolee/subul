var today = new Date();
$('input[name="display_date"]').val(today.yyyymmdd());

function getTableList() {
    $.ajax({
        url: '/labor/release',
        type: 'get',
        data: {display_date: $('input[name="display_date"]').val()},
    }).done(function (data) {
        $("div.table").html(data.list);
    });
}

$('input[name="display_date"]').change(function () {
   getTableList();
});

// setInterval(getTableList, 10000);


