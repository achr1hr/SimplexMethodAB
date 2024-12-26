from TSProgram import TravelingSalesman
from tabulate import tabulate

def start_generation(actual_locs):
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
    inp = input()
    if inp == "go":
        if len(actual_locs)>1:
            start_generation(actual_locs)
            cur_weight = 0
            continue
        else:
            print("Невозможно отправить грузовик")
            continue
    inp = int(inp)
    if inp==0:
        break
    else:
        print("Введите вес запрашиваемого груза")
        weight = int(input())
        if cur_weight+weight < max_weight:
            cur_weight+=weight
            if locs[inp - 1] not in actual_locs:
                actual_locs.append(locs[inp - 1])
            continue
        if cur_weight+weight == max_weight:
            cur_weight = 0
            if locs[inp - 1] not in actual_locs:
                actual_locs.append(locs[inp - 1])
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

