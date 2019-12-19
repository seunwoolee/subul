class Main {
    constructor() {
        this.setDateClickEventHandler();
        this.setBoxIconClickEventHandler();
        this.setCreateClickEventHandler();
        this.setCarRowClickEventHandler();
        this.setLocationRowClickEventHandler();
        this.location = new Location();
        this.car = new Car();
        this.dragDrop = new DragDrop('.dragdrop','.dragdrop');
    }

    initData() {
        $("#order-list-row .card").remove();
        this.getLocationTable();
    }

    setDateClickEventHandler() {
        $('#order_date').change( () => {
            this.initData();
            this.getCarTable();
            $('#pallet-list i').remove();
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
        });
    }

    setBoxIconClickEventHandler() {
        $(document).on('click', '.box-icon', event => {
            let location_id = null;
            let pallet_id = $(event.currentTarget).attr('data-pallet-id');
            let ymd = set_yyyymmdd($('#order_date').val());

            this.location.getLoadedItems(location_id, pallet_id, ymd)
                .then(data => {
                    $("#pallet-bin").html(data['list']);
                    $('.box-icon').css('color','rgb(0, 0, 0)').removeAttr('data-selected');
                    $('.box-icon[data-pallet-id='+pallet_id+']').css('color', 'red').attr('data-selected', true);
                    main.dragDrop.setDragDrop('[class*=col]','.card-header','.dragdrop');
                    main.dragDrop.getSumAmount();
                })
                .catch( () => alert('수정 에러 전산실로 문의바랍니다.'))
        });
    }

    setCarRowClickEventHandler(){
        $(document).on('click', ".car-item tbody tr", (event) => {
            this.car.getPalletList(this.car.carTable.row(event.currentTarget).data()['id'])
                .then((data)=>{
                    $("#pallet-list").html(data['list']);
                    $('[data-toggle="tooltip"]').tooltip('dispose');
                    $('[data-toggle="tooltip"]').tooltip({delay: {"hide": 800 }});
                })
        });
    }

    setLocationRowClickEventHandler(){
        $(document).on('click', ".location-item tbody tr", (event) => {
            let location_id = this.location.locationTable.row(event.currentTarget).data()['orderLocationCode'];
            let selectedIndex = this.location.locationTable.row(event.currentTarget).index();
            let ymd = set_yyyymmdd($('#order_date').val());
            let pallet_id = $('.box-icon[data-selected='+true+']').attr('data-pallet-id');
            let isBoxSelected = $('.box-icon[data-selected='+true+']').length;

            if(isBoxSelected) {
                $('.loader-backdrop').css('display', 'block');

                this.location.loadItems()
                    .then(()=>this.location.getUnloadedItems(location_id, pallet_id, ymd))
                    .then( (data) => {
                        $("#order-list-row").html(data['list']);
                    })
                    .then(() => this.car.getPalletList(this.car.carTable.row('.selected').data()['id']))
                    .then((data)=> {
                        $("#pallet-list").html(data['list']);
                        $('[data-toggle="tooltip"]').tooltip('dispose');
                        $('[data-toggle="tooltip"]').tooltip({delay: {"hide": 800 }});
                        $('.loader-backdrop').css('display', 'none');
                        this.dragDrop.setDragDrop('[class*=col]','.card-header','.dragdrop');
                        this.location.locationTable.ajax.reload(() => {
                            const row = this.location.locationTable.row(selectedIndex).node();
                            $(row).addClass('selected');
                        })
                    })
                    .catch((err)=>{
                        $('.loader-backdrop').css('display', 'none');
                        console.log(err);
                    })
            } else {
                alert('차량선택 후 팔레트를 선택해주세요.');
                return false;
            }
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
            placeholder: 'card-placeholder',
            stop: (event, ui) => {
                this.getSumAmount();
            }
        }).disableSelection();
    }

    getSumAmount () {
        const reducer = (accumulator, currentValue) => accumulator + currentValue;
        const rows = [...document.querySelectorAll('#pallet-bin .col-md-12')];
        const kgAmount = rows.map(row => Number(row.dataset.amount));
        const oneKgAmount = rows.filter(row => Number(row.dataset.amountType) === 1.00)
            .map(row => Number(row.dataset.amount));
        const fiveKgAmount = rows.filter(row => Number(row.dataset.amountType) === 5.00)
            .map(row => Number(row.dataset.amount));
        let sumKgAmount = 0;
        let sumOneKgAmount = 0;
        let sumFiveKgAmount = 0;
        if(kgAmount.length){
            sumKgAmount = kgAmount.reduce(reducer)
        }
        if(oneKgAmount.length){
            sumOneKgAmount = oneKgAmount.reduce(reducer)
        }
        if(fiveKgAmount.length){
            sumFiveKgAmount = fiveKgAmount.reduce(reducer)
        }

        $('#sumOneKgAmount').text(sumOneKgAmount);
        $('#sumFiveKgAmount').text(sumFiveKgAmount);
        $('#sumKgAmount').text(sumKgAmount);
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

    getPalletList(car_id){
        let ymd = set_yyyymmdd($('#order_date').val());
        let selectPallet_id = $(".box-icon[data-selected=true]").attr('data-pallet-id');

        return $.ajax({
            url: '/release/releaseOrderCar',
            type: 'get',
            data: {'car_id': car_id, 'pallet_id': selectPallet_id ,'ymd': ymd},
        })
    }
}

class Location {

    getLocationDataTable(ymd) {
        this.locationTable = $('.location-item').DataTable({
            "language": {
                searchPlaceholder: "거래처명",
                infoFiltered: "",
                info: "",
                emptyTable: "데이터를 생성해주세요",
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
                {"data": "total_count"},
                {"data": "is_unloaded"},
            ],
            dom: 'Bfrtip',
            buttons: [],
        });
    }

    getUnloadedItems (location_id, pallet_id, ymd) {
        return $.ajax({
            url: '/release/releaseOrder',
            type: 'get',
            data: {'location_id': location_id, 'pallet_id': pallet_id, 'ymd': ymd, 'type': 'unloaded'},
        })
    }

    getLoadedItems (location_id, pallet_id, ymd) {
        return $.ajax({
            url: '/release/releaseOrder',
            type: 'get',
            data: {'location_id': location_id, 'pallet_id': pallet_id, 'ymd': ymd, 'type': 'loaded'},
        })
    }

    loadItems () {
        let selectPallet_id = $(".box-icon[data-selected=true]").attr('data-pallet-id');
        if(selectPallet_id){
            let data = {'pallet_id': selectPallet_id};
            data['order_list_id'] = $('#pallet-bin').serializeArray().map(objects => objects['value']).join();
            return $.ajax({
                url: '/release/releaseOrderCar',
                type: 'post',
                data: data,
            })
        } else {
            alert('차량선택 및 팔레트를 선택해주세요.');
        }
    }
}

main = new Main();
