let myFullCalendar = null;
getAudit().then(rows => {
    const events = [];
    for (const rowsKey in rows) {
        const temp = {
            start: moment(rows[rowsKey].ymd, "YYYYMMDD").format('YYYY-MM-DD'),
            end: moment(rows[rowsKey].ymd, "YYYYMMDD").format('YYYY-MM-DD'),
            title: moment(rows[rowsKey].ymd, "YYYYMMDD").format('YYYY-MM-DD') + ' 마감',
        }
        events.push(temp);
    }
    createFullCalendar(events);
});

function getAudit() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/api/get_audit/',
            type: 'GET',
        }).done(function (data) {
            resolve(data);
        })
    })
}

function createFullCalendar(events) {
    myFullCalendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            right: ''
        },
        defaultDate: moment().format('YYYY-MM-DD'),
        dayClick(date, jsEvent, view, resourceObj) {
            if (confirm("월 마감을 실시 하시겠습니까?")) {

                $.ajax({
                    url: '/api/audit/',
                    type: 'POST',
                    data: {"ymd": date.format('YYYYMMDD')},
                }).done(function (data) {
                    location.reload();
                }).fail(function (xhr, status, error) {
                    alert('에러발생! 전산팀으로 문의 바랍니다.');
                });
            }
        },
        editable: true,
        eventLimit: true,
        events: events
    });
}
