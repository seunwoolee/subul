$(function () {

    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });

});

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

$(document).on('click', '.MODIFY', function () {
    let parentDiv = $(this).closest('div');
    let id = parentDiv.attr('data-id');
    let boxCount = parentDiv.attr('data-boxCount');
    let eaCount = parentDiv.attr('data-eaCount');

    $('#modifyModal form').attr('action', '/api/productOrderPacking/' + id);

    $('#id_boxCount').val(boxCount);
    $('#id_eaCount').val(eaCount);
    $("#modifyModal").modal();
});

$(document).on('click', '.REMOVE', function () {
    let parentDiv = $(this).closest('div');
    let id = parentDiv.attr('data-id');
    $('#confirm form').attr('action', '/api/productOrderPacking/' + id);

    $('#modal_title').text('DELETE');
    $("#confirm").modal();
});

// $(document).on('click', 'MODIFY-PARENT', function () {
//     let parentDiv = $(this).closest('div');
//     let id = parentDiv.attr('data-id');
//     $('#confirm form').attr('action', '/api/productOrderPacking/' + id);
//
//     $('#modal_title').text('DELETE');
//     $("#confirm").modal();
// });

// function deleteButtonClick(data) {
//
//     $('#modal_title').text('DELETE');
//     $("#confirm").modal();
// }


$(document).on('submit', 'form', function (e)
{
    e.preventDefault();

    let data = $(this).serialize();
    let type = $(this).find('.ajaxUrlType').val();
    let url = $(this).attr('action');

    $.ajax({
        url: url,
        type: type,
        data: data,
    }).done(function (data) {
        alert('완료');
        location.reload();
    }).fail(function () {
        alert('에러발생! 전산팀으로 문의 바랍니다.');
    });
});
