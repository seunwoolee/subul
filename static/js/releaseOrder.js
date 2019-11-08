class Main {
    constructor() {
        this.setDateClickEventHandler();
        this.location = new Location();
    }

    setDateClickEventHandler() {
        $('#order_date').change( () => {

            if(this.location.locationTable){
                this.location.locationTable.destroy();
            }

            this.location.getLocationDataTable(set_yyyymmdd($('#order_date').val()));
            $('.location-item').show();
        });
    }

}

class DragDrop {
    constructor(element, handle, connect){
        this.element = element;
        this.handle = handle;
        this.connect = connect;
        this.setDragDrop();
    }

    setDragDrop(){
        $(this.element).sortable({
            handle: this.handle,
            connectWith: this.connect,
            tolerance: 'pointer',
            forcePlaceholderSize: true,
            opacity: 0.8,
            placeholder: 'card-placeholder'
        }).disableSelection();
    }
}

class Car {
    constructor() {
        this.getCarDataTable();
        this.setClickEventHandler();
    }

    getCarDataTable() {
        this.carTable = $('.car-item').DataTable({
            "language": {
                searchPlaceholder: "차량번호",
                infoFiltered: "",
                info: "",
                select: {
                    rows: ""
                },
            },
            "paging": false,
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": "/api/releaseOrderCar/?format=datatables",
                "type": "GET"
            },
            "responsive": true,
            "select": true,
            "columns": [
                {"data": "car_number"},
                {"data": "type", searchable: false},
                {"data": "palette_count", searchable: false},
            ],
            dom: 'Bfrtip',
            buttons: [],
        });
    }

    setClickEventHandler(){
        $(document).on('click', ".car-item tbody tr", function () {
            alert();
            // let data = carTable.row($(this)).data();
            // setNormalLocationStyle();
            // manualReleaseModal(data);
        });
    }
}

class Location {

    getLocationDataTable(ymd) {
        this.locationTable = $('.location-item').DataTable({
            "language": {
                searchPlaceholder: "거래처명",
                infoFiltered: "",
                info: "",
                select: {
                    rows: ""
                },
            },
            "paging": false,
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": "api/releaseOrderLocation/?ymd="+ymd+"&format=datatables",
                "type": "GET"
            },
            "responsive": true,
            "select": true,
            "columns": [
                {"data": "orderLocationName"},
            ],
            dom: 'Bfrtip',
            buttons: [],
        });
    }

    // getLocationDataTable(ymd) {
    //     $('#stepOne .datatable').DataTable().search($("input[type='search']").val()).draw();
    // }
}

main = new Main();
car = new Car();
dragDrop = new DragDrop('[class*=col]','.card-header','.dragdrop');
// location = new Location();
