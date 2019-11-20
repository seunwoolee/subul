class Main {
    constructor() {
        $('#order_date').val(end_day);
        this.setDateClickEventHandler();
        this.setLoadButtonClickEventHandler();
        this.setBoxIconClickEventHandler();
        this.setCreateClickEventHandler();
        this.location = new Location();
        this.location.setClickEventHandler();
        this.car = new Car();
        this.car.setClickEventHandler();
        this.dragDrop = new DragDrop('.dragdrop','.dragdrop');
    }

    setDateClickEventHandler() {
        $('#order_date').change( () => {
            this.initData();
            this.getCarTable();
            $('#pallet-list i').remove();
        });
    }

    initData() {
        $("#order-list-row .card").remove();
        this.getLocationTable();
    }

    setLoadButtonClickEventHandler() {

        $('.load-button').click( () => {
            let that = this;
            debugger;
            let selectPallet_id = $(".box-icon[data-selected=true]").attr('data-id');
            if(selectPallet_id) {
                let data = {'pallet_id': selectPallet_id};
                data['order_list_id'] = $('#pallet-bin').serializeArray().map(objects => objects['value']).join();
                $.ajax({
                    url: '/release/releaseOrderCar',
                    type: 'post',
                    data: data,
                }).done(function (data) {
                    that.initData();
                    that.car.getPalletList(that.car.carTable.row('.selected').data()['id']);
                    $('#pallet-bin div').remove();
                }).fail(function () {
                    alert('수정 에러 전산실로 문의바랍니다.');
                });
            } else {
                alert('차량선택 및 팔레트를 선택해주세요.')
            }
        });
    }

    setCreateClickEventHandler() {
        $('.create').click( () => {
            let ymd = set_yyyymmdd($('#order_date').val());
            let that = this;
            if(confirm($('#order_date').val()+' 출고 내역을 생성 하시겠습니까?')) {
                $.ajax({
                    url: '/release/releaseOrder',
                    type: 'post',
                    data: {'ymd': ymd},
                }).done(function (data) {
                    that.getLocationTable();
                    alert('성공');
                }).fail(function () {
                    alert('수정 에러 전산실로 문의바랍니다.');
                });
            }
            // this.getLocationTable();
        });
    }

    setBoxIconClickEventHandler() {
        $(document).on('click', '.tooltip-inner .change', event => {
            console.log($(event.currentTarget));
        });

        $(document).on('click', '.tooltip-inner .see', event => {
            let id = $(event.currentTarget).attr('data-pallet-id');
            let ymd = set_yyyymmdd($('#order_date').val());
            $.ajax({
                url: '/release/releaseOrder',
                type: 'get',
                data: {'id': id, 'ymd': ymd, 'type': 'loaded'},
            }).done(function (data) {
                $("#pallet-bin").html(data['list']);
                $('.box-icon').css('color','rgb(0, 0, 0)').removeAttr('data-selected');
                $('i[data-id='+id+']').css('color', 'red').attr('data-selected', true);
                main.dragDrop.setDragDrop('[class*=col]','.card-header','.dragdrop');
            }).fail(function () {
                alert('수정 에러 전산실로 문의바랍니다.');
            });
        });
    }

    getCarTable() {
        if(this.car.carTable){
            this.car.carTable.destroy();
        }
        this.car.getCarDataTable();
        $('.car-item').show();
    }

    getLocationTable() {
        if(this.location.locationTable){
            this.location.locationTable.destroy();
        }
        this.location.getLocationDataTable(set_yyyymmdd($('#order_date').val()));
        $('.location-item').show();
    }
}

class DragDrop {
    constructor(element, connect){
        this.element = element;
        this.connect = connect;
        this.setDragDrop();
    }

    setDragDrop(){
        $(this.element).sortable({
            connectWith: this.connect,
            tolerance: 'pointer',
            forcePlaceholderSize: true,
            opacity: 0.8,
            placeholder: 'card-placeholder'
        }).disableSelection();
    }
}

class Car {

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
                {"data": "id", visible: false, searchable: false},
                {"data": "car_number"},
                {"data": "type", searchable: false},
                {"data": "pallet_count", searchable: false},
            ],
            dom: 'Bfrtip',
            buttons: [],
        });
    }

    setClickEventHandler(){
        $(document).on('click', ".car-item tbody tr", (event) => {
            this.getPalletList(this.carTable.row(event.currentTarget).data()['id']);
        });
    }

    getPalletList(car_id){
        let ymd = set_yyyymmdd($('#order_date').val());
        $.ajax({
            url: '/release/releaseOrderCar',
            type: 'get',
            data: {'id': car_id, 'ymd': ymd},
        }).done(function (data) {
            $("#pallet-list").html(data['list']);
            $('[data-toggle="tooltip"]').tooltip('dispose');
            $('[data-toggle="tooltip"]').tooltip({delay: {"hide": 800 }});
        }).fail(function () {
            alert('수정 에러 전산실로 문의바랍니다.');
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
                {"data": "orderLocationCode"},
                {"data": "orderLocationName"},
            ],
            dom: 'Bfrtip',
            buttons: [],
        });
    }

    setClickEventHandler(){
        $(document).on('click', ".location-item tbody tr", (event) => {
            let id = this.locationTable.row(event.currentTarget).data()['orderLocationCode'];
            let ymd = set_yyyymmdd($('#order_date').val());
            let isBoxSelected = $('.box-icon[data-selected='+true+']').length;

            if(isBoxSelected) {
                if(confirm('주문 내역을 불러 오시겠습니까?')) {
                    $.ajax({
                        url: '/release/releaseOrder',
                        type: 'get',
                        data: {'id': id, 'ymd': ymd, 'type': 'unloaded'},
                    }).done(function (data) {
                        $("#order-list-row").html(data['list']);
                        main.dragDrop.setDragDrop('[class*=col]','.card-header','.dragdrop');
                    }).fail(function () {
                        alert('수정 에러 전산실로 문의바랍니다.');
                    });
                }
            } else {
                alert('차량선택 후 팔레트를 선택해주세요.');
            }

        });
    }

}

main = new Main();
