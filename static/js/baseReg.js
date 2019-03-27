if(!SUPERUSER)
{
    if(today <= getMiddleDay(today))
    {
        $('input[type=date]').attr("min",getPreviousMonthFirstDay(today));
    }
    else
    {
        $('input[type=date]').attr("min",getFirstDay(today));
    }
}
