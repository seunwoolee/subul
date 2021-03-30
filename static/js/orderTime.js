$(function () {
    $('.start, .end').timepicker({
        timeFormat: 'HH:mm',
        interval: 60,
        minTime: '00',
        maxTime: '23',
        defaultTime: '00',
        startTime: '00',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });
});

SEQ = 2;

function cloneMore(selector, prefix) {
    $(selector).find('.company').select2("destroy");
    $(selector).find('.start').data('TimePicker').destroy();
    $(selector).find('.end').data('TimePicker').destroy();
    let newElement = $(selector).clone(true);
    let previousCompanyValue = $(selector).find('.company').val();
    let no = newElement.find('.no');
    let total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    newElement.find(':input').each(function () {
        setNewElementInputInfo($(this), total, previousCompanyValue);
    });

    total++;
    no.html(SEQ).css("background-color", "");
    SEQ++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    let conditionRow = $('.forms-row:not(:last)');
    minusConditionRow(conditionRow, 'normal');
    $('.django-select2').djangoSelect2();
    newElement.find('.start, .end').timepicker({
        timeFormat: 'HH:mm',
        interval: 60,
        minTime: '00',
        maxTime: '23',
        defaultTime: '00',
        startTime: '00',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });
    return false;
}

function setNewElementInputInfo($this, total, previousCompanyValue) {
    var name = $this.attr('name');
    if (name) {
        name = name.replace('-' + (total - 1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $this.attr({'name': name, 'id': id});
        if (name.indexOf("company") >= 0) {
            $this.attr({'name': name, 'id': id}).val(previousCompanyValue).trigger('change');
        }
        // {
        //     $this.attr({'name': name, 'id': id}).val(previousLocationValue).trigger('change');
        // }
        // if (name.indexOf("type") >= 0 || name.indexOf("set") >= 0 || name.indexOf("specialTag") >= 0) {  // 타입,일반/특인,세트는 판매로 고정한다(사용자 편의)
        //     $this.attr({'name': name, 'id': id});
        // } else if (name.indexOf("location") >= 0) // 그 전의 location을 그대로 가져온다(사용자 편의)
        // {
        //     $this.attr({'name': name, 'id': id}).val(previousLocationValue).trigger('change');
        // } else if (name.indexOf("product") >= 0) // 이전의 제품 option 값 지우기
        // {
        //     $this.attr({'name': name, 'id': id}).find('option').remove();
        // } else {
        //     $this.attr({'name': name, 'id': id}).val('').removeAttr('checked');
        // }

        // if (name.indexOf("start") >= 0) {
        //     $('#' + id).timepicker({
        //         timeFormat: 'HH:mm',
        //         interval: 60,
        //         minTime: '00',
        //         maxTime: '23',
        //         defaultTime: '00',
        //         startTime: '00',
        //         dynamic: false,
        //         dropdown: true,
        //         scrollbar: true
        //     });
        // }

    }
}

function minusConditionRow(conditionRow, type) {
    if (type == "normal") {
        conditionRow = conditionRow.find('.btn.add-form-row');
    }
    conditionRow.removeClass('btn-success').removeClass('btn-dark').addClass('btn-danger')
        .removeClass('add-form-row').removeClass('add-form-set').addClass('remove-form-row')
        .html('-');
}

function plusConditionRow(conditionRow) {
    conditionRow.removeClass('btn-dark').removeClass('btn-danger')
        .addClass('btn-success')
        .removeClass('remove-form-row').removeClass('add-form-set')
        .addClass('add-form-row').html('+');
}

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1) {
        btn.closest('.forms-row').remove();
        let forms = $('.forms-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (let i = 0; i < forms.length; i++) {
            $(forms.get(i)).find(':input').each(function () {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

$(document).on('click', '.add-form-row', function (e) { //일반상품 + 버튼
    e.preventDefault();
    let parentTR = $(this).parents('tr');

    if ($('form')[0].checkValidity()) {
        cloneMore('.forms-row:last', 'form');
        setReadOnly($(this).parents('tr'));
    } else {
        alert('정보를 모두 알맞게 넣어주세요(빨간색->녹색)');
    }

    return false;
});

$(document).on('click', '.remove-form-row', function (e) { // 삭제 - 버튼
    e.preventDefault();
    deleteForm('form', $(this));
    calculatePriceCount();
    return false;
});

$(document).on('click', '#deleteLastButton', function (e) {
    if (confirm('마지막 줄을 지우시겠습니까?')) {
        let lastButton = $('.add-form-row');
        e.preventDefault();
        deleteForm('form', lastButton);

        if ($('.add-form-row').length === 0) {
            let lastTR = $('.forms-row:last');
            lastTR.find('.start, .end, .weekday').each(function () {
                $(this).attr('disabled', false);
            });
            lastTR.find('.weekday').attr('readonly', false);
            lastTR.find('.django-select2').prop("disabled", false);
            plusConditionRow(lastTR.find('.remove-form-row'));

        }
    }
    return false;
});

$("#submitButton").click(function (e) {
    e.preventDefault();
    if ($('form')[0].checkValidity()) {
        $("input:disabled").prop('disabled', false);
        $('.django-select2').prop("disabled", false);
        $("form").submit();
    } else {
        alert('모든칸을 다 입력해주세요');
    }

});


function setReadOnly($parentTR) {
    $parentTR.find('.start, .end').each(function () {
        $(this).attr('disabled', 'true');
    });
    $parentTR.find('.weekday').each(function () {
        $(this).attr('readonly', 'true');
    });
    $parentTR.find('.django-select2').each(function () {
        $(this).prop("disabled", true);
    });
}
