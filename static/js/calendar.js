$('#calendar').fullCalendar({
    header: {
        left: 'prev,next today',
        right: ''
    },
    defaultDate: moment().format('YYYY-MM-DD'),
    dayClick(date, jsEvent, view, resourceObj) {
        if (confirm("월 마감을 실시 하시겠습니까?")) {

            $.ajax({
                url: '/api/createAudit/',
                type: 'POST',
                data: {"ymd": date.format('YYYYMMDD')},
            }).done(function (data) {
                alert('완료');
                // $('.datatable').DataTable().search($("input[type='search']").val()).draw();
                // $(".everyModal").modal('hide');
            }).fail(function (xhr, status, error) {
                alert('에러발생! 전산팀으로 문의 바랍니다.');
            });
        }
    },
    editable: true,
    eventLimit: true,
    events: [{
        title: 'All Day Event',
        start: '2016-01-01'
    }, {
        title: 'Long Event',
        start: '2016-01-07',
        end: '2016-01-10'
    }, {
        id: 999,
        title: 'Repeating Event',
        start: '2016-01-09T16:00:00'
    }, {
        id: 999,
        title: 'Repeating Event',
        start: '2016-01-16T16:00:00'
    }, {
        title: 'Conference',
        start: '2016-01-11',
        end: '2016-01-13'
    }, {
        title: 'Meeting',
        start: '2016-01-12T10:30:00',
        end: '2016-01-12T12:30:00'
    }, {
        title: 'Lunch',
        start: '2016-01-12T12:00:00'
    }, {
        title: 'Meeting',
        start: '2016-01-12T14:30:00'
    }, {
        title: 'Happy Hour',
        start: '2016-01-12T17:30:00'
    }, {
        title: 'Dinner',
        start: '2016-01-12T20:00:00'
    }, {
        title: 'Birthday Party',
        start: '2016-01-13T07:00:00'
    }, {
        title: 'Click for Google',
        url: 'http://google.com/',
        start: '2016-01-28'
    }]
})
;
//# sourceMappingURL=calendar.js.map
