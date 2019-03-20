/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.1.1): datatables.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

 $(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }


hotkeys('BackSpace,f5', function(event, handler) {
  // Prevent the default refresh event under WINDOWS system
  event.preventDefault();
});

Date.prototype.yyyymmdd = function() {
  var mm = this.getMonth() + 1;
  var dd = this.getDate();
  return [this.getFullYear(), (mm>9 ? '' : '0') + mm,  (dd>9 ? '' : '0') + dd ].join('-');
};

function getDayOfWeek(date)
{
    let weekArray = [
        '일',
        '월',
        '화',
        '수',
        '목',
        '금',
        '토'
    ];
    let dayOfweek = new Date(date).getDay();
    if(isNaN(dayOfweek))
    {
        return false;
    }
    else
    {
        return weekArray[dayOfweek]
    }
}

function set_yyyymmdd(yyyy_mm_dd)
{
    temp = yyyy_mm_dd.split('-');
    return yyyyymmdd = temp[0]+temp[1]+temp[2];
}

function set_yyyy_mm_dd(yyyymmdd)
{
    if(yyyymmdd != null)
    {
        if (yyyymmdd.length == 8)
        {
            let yyyy = yyyymmdd.substring(0, 4);
            let mm = yyyymmdd.substring(4, 6);
            let dd = yyyymmdd.substring(6, 8);
            return fakeYmd = yyyy + '-' + mm + '-' + dd;
        }
    }
    else
    {
        return yyyymmdd;
    }
}
var date = new Date();
var days = 7;
var minusSevenDate = new Date(date.getTime() - (days * 24 * 60 * 60 * 1000));
var plusThreeDate = new Date(date.getTime() + (3 * 24 * 60 * 60 * 1000));
var minusFifteenDate = new Date(date.getTime() - (15 * 24 * 60 * 60 * 1000));

var start_day = minusSevenDate.yyyymmdd();
var end_day = date.yyyymmdd();
var plusThree_day = plusThreeDate.yyyymmdd();
var minusFifteen_day = set_yyyymmdd(minusFifteenDate.yyyymmdd());
var today = set_yyyymmdd(date.yyyymmdd());

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function setDataTableActionButtonWithPdf()
{
    return '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="far fa-trash-alt"></i></button>' +
            '<button class="btn btn-info btn-sm MODIFY" href="#"><i class="fa fa-edit"></i></button>'+
            '<button class="btn btn-warning btn-sm PDF" href="#"><i class="fas fa-file-pdf"></i></button>';
}

function setDataTableActionButtonWithoutEdit()
{
    return '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="far fa-trash-alt"></i></button>' +
            '<button class="btn btn-warning btn-sm PDF" href="#"><i class="fas fa-file-pdf"></i></button>';
}

function setDataTableActionButtonOnlyDelete()
{
    return '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="far fa-trash-alt"></i></button>';
}

function setDataTableActionButtonOnlyPdf()
{
    return '<button class="btn btn-warning btn-sm PDF" href="#"><i class="fas fa-file-pdf"></i></button>';
}

function setDataTableActionButton()
{
    return '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="far fa-trash-alt"></i></button>' +
            '<button class="btn btn-info btn-sm MODIFY" href="#"><i class="fa fa-edit"></i></button>';
}

function setDataTableActionButtonOnlyModify()
{
    return '<button class="btn btn-info btn-sm MODIFY" href="#"><i class="fa fa-edit"></i></button>';
}

function setDataTableActionButtonWithRecall()
{
    return '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="far fa-trash-alt"></i></button>' +
            '<button class="btn btn-info btn-sm MODIFY" href="#"><i class="fa fa-edit"></i></button>' +
            '<button class="btn btn-success btn-sm RECALL" href="#"><i class="fas fa-undo-alt"></i></button>';
}

function setDataTableActionButtonWithPdfRecall()
{
    return '<button class="btn btn-danger btn-sm REMOVE" href="#"><i class="far fa-trash-alt"></i></button>' +
            '<button class="btn btn-warning btn-sm PDF" href="#"><i class="fas fa-file-pdf"></i></button>' +
            '<button class="btn btn-success btn-sm RECALL" href="#"><i class="fas fa-undo-alt"></i></button>';
}

 $('.input-daterange input:text').datepicker({
  todayBtn:'linked',
  format: "yyyymmdd",
  autoclose: true
 });

function setAutoCountValue($this)
{
    if($this.val().length > 0)
    {
        parentTR = $this.parents('tr');
        amount = $this.val();
        count = amount / window.AMOUNT_KG['AMOUNT_KG'];
        count = Math.round(count * 100) / 100;
        parentTR.find('.count').val(count);
        parentTR.find('.amount_kg').val(window.AMOUNT_KG['AMOUNT_KG']);
    }
}

function setAutoAmountValue($this)
{
    if($this.val().length > 0)
    {
        parentTR = $this.parents('tr');
        count = $this.val();
        amount = count * window.AMOUNT_KG['AMOUNT_KG'];
        amount = Math.round(amount * 100) / 100;
        parentTR.find('.amount').val(amount);
        parentTR.find('.amount_kg').val(window.AMOUNT_KG['AMOUNT_KG']);
    }
}

function setSpecialTagButton(data)
{
    if(data == "특인가")
    {
        return '<button class="btn btn-danger btn-sm">'+ data +'</button>';
    }
    else
    {
        return '';
    }
}

function autoSetEndDate(e)
{
    $('#end_date').val(e.target.value);
}

function getYearMonth(yyyymmdd)
{
    return parseInt(yyyymmdd.substring(0,6));
}

function getMonth(yyyymmdd)
{
    return parseInt(yyyymmdd.substring(4,6));
}

function getYear(yyyymmdd)
{
    return parseInt(yyyymmdd.substring(0,4));
}

function getMiddleDay(yyyymmdd)
{
    return yyyymmdd.substring(0,6)+"15";
}