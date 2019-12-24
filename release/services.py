from .models import Release, OrderList, Car, Pallet


class CarServices():

    def save_pallet(self, pallet_count: int, car: Car) -> bool:
        for seq in range(int(pallet_count)):
            Pallet(**{'car': car, 'seq': seq+1}).save()
        return True
