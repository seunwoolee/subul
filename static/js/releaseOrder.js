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
        this.setCarDataTable();
        this.setClickEvent();
    }

    setCarDataTable() {
        this.carTable = $('.car-item').DataTable({
            "language": {
                searchPlaceholder: "차량번호",
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
    setClickEvent(){
        $(document).on('click', ".car-item tbody tr", function () {
            alert();
            // let data = carTable.row($(this)).data();
            // setNormalLocationStyle();
            // manualReleaseModal(data);
        });
    }
}

car = new Car();
dragDrop = new DragDrop('[class*=col]','.card-header','[class*=col]');
