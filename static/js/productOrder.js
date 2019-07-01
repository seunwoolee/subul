$('#start_date').val(end_day);
$('#create').click(function () {
    let start_date = set_yyyymmdd($('#start_date').val());
    let end_date = set_yyyymmdd(plusSeven_day);
    let content_type = 'other'
    if(confirm(`${start_date} 생산지시를 하시겠습니까?`)){

        if(confirm(`전란 생산을 지시하시겠습니까`)){
            content_type = '전란'
        }

        $.ajax({
        url: 'product/order',
        type: 'post',
        data: {'start_date': start_date, 'end_date': end_date, 'content_type': content_type},
        }).done(function(data) {
            alert('완료');
        }).fail(function(e) {
            alert('수정 에러 전산실로 문의바랍니다.');
        });

    }
});
