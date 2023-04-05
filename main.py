from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, items, capacity):
        self._items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, name, count):
        pass

    @abstractmethod
    def remove(self, name, count):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):

    def __init__(self, items, capacity=100):
        super().__init__(items, capacity=100)

    def add(self, name, count):
        if count > self._capacity:
            return False
        if name not in self._items:
            self._items[name] = 0

        self._items[name] += count
        self._capacity -= count


    def remove(self, name, count):
        if name not in self._items:
            return False
        if self._items[name] - count < 0:
            return False
        else:
            self._items[name] -= count
            self._capacity += count

    def get_free_space(self):
        return self._capacity

    def get_items(self):
        return self._items

    def get_unique_items_count(self):
        return len(self._items)


class Shop(Store):
    def __init__(self, items):
        self._items = items
        self._capacity = 20
        self._names = 5

    def add(self, name, count):
        if count > self._capacity:
            return False
        if len(self._items) == 5 and name not in self._items:
            return False
        if name not in self._items:
            self._items[name] = 0
        self._items[name] += count
        self._capacity -= count

    def remove(self, name, count):
        if name not in self._items:
            return False
        if self._items[name] - count < 0:
            return False
        else:
            self._items[name] -= count
            self._capacity += count

class Request:
    def __init__(self, string):
        self._from = string.split()[4]
        self._to = string.split()[6]
        self._amount = int(string.split()[1])
        self._product = string.split()[2]

    @property
    def to(self):
        return self._to

    @property
    def from_(self):
        return self._from

    @property
    def amount(self):
        return self._amount

    @property
    def product(self):
        return self._product

    def delivery(self, store, shop):
        if self._from == 'склад':
            if self._product not in store.get_items():
                return 'Нет на складе, попробуйте заказать меньше'

            if store.remove(self._product, self._amount) == False:
                return 'Не хватает на складе, попробуйте заказать меньше'

            if shop.add(self._product, self._amount) == False:
                return 'нельзя добавить в магазин'
            else:
                return True

        if self._from == 'магазин':
            if self._product not in shop.get_items():
                return 'Нет в магазине, попробуйте заказать меньше'
            if shop.remove(self._product, self._amount) == False:
                return 'Не хватает в магазине, попробуйте заказать меньше'
            if store.add(self._product, self._amount) == False:
                return 'нельзя добавить на склад'

            else:
                return True


def main():
    store = Store(
        {
            'мандарины': 3,
            'мороженое': 2,
            'пончики': 4
        }
    )
    shop = Shop(
        {
            'конфеты': 2,
            'сок': 4,
            'бананы': 1
        }
    )

    req = Request(input())
    if req.delivery(store, shop) == True:
        print(f'Нужное количество есть на {req.from_}')
        print(f'Курьер забрал {req.amount} {req.product} со {req.from_}')
        print(f'Курьер везет {req.amount} {req.product} со {req.from_} в {req.to}')
        print(f'Курьер доставил {req.amount} {req.product} в {req.to}')
        print(f'на складе {store.get_items()}')
        print(f'в магазине {shop.get_items()}')
    else:
        print(req.delivery(store, shop))
        print(f'на складе {store.get_items()}')
        print(f'в магазине {shop.get_items()}')
        exit()



if __name__ == '__main__':
    main()
