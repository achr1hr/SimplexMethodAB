from importlib.metadata import pass_none

from TSProgram import TravelingSalesman
from tabulate import tabulate

print("Введите адрес склада")
whouse_loc = input()
print("Введите количество магазинов")
shops = int(input())
print(f"Введите адреса магазинов {shops} раз без точек, запятых и прочих спец-символов")
locs = []
for i in range(shops):
    a = input()
    locs.append(a)
print("Введите грузоподъёмность грузовика")
max_weight = int(input())
cur_weight = 0
actual_locs = [whouse_loc]
while True:
    print(f"Заполненность грузовика: {cur_weight}/{max_weight}")
    print("Выберите магазин:")
    for i, loc in enumerate(locs):
        print(f"{i+1}. ", loc)
    print("Для выхода введите 0.", "Для отправления грузовика напишите 'go' ", sep='\n')
    inp = int(input())
    if inp==0:
        break
    else:
        if locs[inp - 1] not in actual_locs:
            actual_locs.append(locs[inp-1])
        if inp!="go":
            print("Введите вес запрашиваемого груза")
            weight = int(input())
        else:
            print("Генерация маршрута...")
        if cur_weight+weight < max_weight and inp!='go':
            cur_weight+=weight
            continue
        if cur_weight+weight == max_weight:
            cur_weight = 0
            print("Грузовик полностью заполнен. Генерация маршрута...")
        elif cur_weight+weight > max_weight:
            cur_weight=weight
            print("Груз не помещается в грузовик. Данный груз будет отправлен в следующем грузовике. Генерация маршрута...")
        TS = TravelingSalesman(actual_locs)
        coords = TS.get_coords()
        matrix = TS.calculate_distance_matrix(coords)
        print("Матрица расстояний")
        print(tabulate(matrix, tablefmt="grid"))
        length, path = TS.solve()
        print(f"Минимальная длина маршрута: {length}")
        print("Маршрут:")
        route_coords = []
        for i in path:
            print(actual_locs[i], " -> ", end='')
            route_coords.append(coords[i])
        print('\n', "Генерация карты...")
        TS.build_route_multiple_points(route_coords)
        actual_locs.clear()
        actual_locs.append(whouse_loc)

