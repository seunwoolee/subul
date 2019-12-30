class Release {
    constructor() {
        const today = new Date();
        $('input[name="display_date"]').val(today.yyyymmdd());

        this.display_date = $('input[name="display_date"]');
        this.display_city = $('select[name="location"]');
        this.display_car = $('select[name="car"]');

        this.setDateChangeHandler();
        this.setLocationChangeHandler();
        this.setCarChangeHandler();
        this.getTableList();
        setInterval(this.getTableList, 10000);
    }

    getTableList = () => {
        $.ajax({
            url: '/labor/release',
            type: 'get',
            data: {
                display_date: this.display_date.val(),
                display_city: this.display_city.val(),
                display_car: this.display_car.val(),
            },
        }).done(function (data) {
            $("div.table").html(data.list);
        });
    };

    setLocationChangeHandler() {
        this.display_city.change(() => {
            this.getTableList();
        });
    }

    setCarChangeHandler() {
        this.display_car.change(() => {
            this.getTableList();
        });
    }

    setDateChangeHandler() {
        this.display_date.change(() => {
            this.getTableList();
        });
    }
}

main = new Release();
