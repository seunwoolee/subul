if(!SUPERUSER)
{
    $('input[type=date]').attr("min",minusFifteenDate.yyyymmdd());
}