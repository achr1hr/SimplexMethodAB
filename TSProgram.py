import osmnx as ox
import folium
import networkx as nx
from geopy.geocoders import Nominatim
from tabulate import tabulate


class TravelingSalesman:
    def __init__(self, locarr):
        self.n = len(locarr)
        self.locarr = locarr[:]
        print(self.locarr)
        self.best_cost = float('inf')
        self.best_path = []


    def get_coords(self):
        coord_arr=[]
        locator = Nominatim(user_agent="myapp")
        for loc in self.locarr:
            location = locator.geocode(loc)
            coord_arr.append((location.latitude,location.longitude))
        return coord_arr

    def calculate_distance_matrix(self, coords_list):
        # Загрузка графа дорог для покрытия всех точек
        central_point = coords_list[0]  # Центральная точка для расчета радиуса
        G = ox.graph_from_point(central_point, dist=50000, network_type='drive')

        # Создаем двумерный массив для расстояний
        n = len(coords_list)
        self.cost_matrix = [[0] * n for _ in range(n)]

        # Поиск ближайших узлов для всех точек
        nodes = [ox.distance.nearest_nodes(G, X=coord[1], Y=coord[0]) for coord in coords_list]

        # Расчет расстояний между каждой парой узлов
        for i in range(n):
            for j in range(n):
                if i != j:
                    try:
                        distance = nx.shortest_path_length(G, nodes[i], nodes[j], weight='length')
                        self.cost_matrix[i][j] = distance/1000  # Преобразуем в километры
                    except nx.NetworkXNoPath:
                        self.cost_matrix[i][j] = float('inf')  # Если путь недоступен
                else:
                    self.cost_matrix[i][j] = float('inf')

        return self.cost_matrix

    def build_route_multiple_points(self, coords_list):
        # Загрузка графа дорог для начальной точки
        G = ox.graph_from_point(coords_list[0], dist=50000, network_type='drive')

        # Создание списка для хранения координат маршрута и расстояний
        route_coords = []
        total_distance = 0  # Общая длина маршрута

        # Пройдем по каждой паре точек и построим маршрут
        for i in range(len(coords_list) - 1):
            start_coords = coords_list[i]
            end_coords = coords_list[i + 1]

            start_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])
            end_node = ox.distance.nearest_nodes(G, X=end_coords[1], Y=end_coords[0])

            route = nx.shortest_path(G, start_node, end_node, weight='length')

            route_coords += [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

            route_length = nx.shortest_path_length(G, start_node, end_node, weight='length')

            print(f"Расстояние от точки {chr(65 + i)} до точки {chr(66 + i)}: {route_length / 1000:.2f} км")

            total_distance += route_length

            if i < len(coords_list) - 2:
                G = ox.graph_from_point(coords_list[i + 1], dist=50000, network_type='drive')

        # Выводим общее расстояние маршрута
        print(f"\nОбщее расстояние маршрута: {total_distance / 1000:.2f} км")

        # Создание карты с центром на первой точке маршрута
        m = folium.Map(location=coords_list[0], zoom_start=13)

        # Добавление маршрута на карту
        folium.PolyLine(route_coords, color="blue", weight=5).add_to(m)

        # Добавление маркеров для всех точек маршрута
        for idx, coords in enumerate(coords_list):
            folium.Marker(coords, popup=f"Point {chr(65 + idx)}",
                          icon=folium.Icon(color="green" if idx == 0 else "red")).add_to(m)

        # Сохранение карты в HTML файл
        m.save("osmnx_route_map.html")
        print("Карта сохранена в файл osmnx_route_map.html")
        return m

    def solve(self):
        initial_bound = self.calculate_initial_bound()
        self.branch_and_bound(0, [0], initial_bound, 0)
        return self.best_cost, self.best_path

    def calculate_initial_bound(self):
        bound = 0
        for i in range(self.n):
            row_min = min(self.cost_matrix[i][j] for j in range(self.n) if i != j)
            bound += row_min
        return bound

    def branch_and_bound(self, level, current_path, current_bound, current_cost):
        if level == self.n - 1:
            last_to_first = self.cost_matrix[current_path[-1]][current_path[0]]
            if last_to_first != float('inf'):
                total_cost = current_cost + last_to_first
                if total_cost < self.best_cost:
                    self.best_cost = total_cost
                    self.best_path = current_path[:] + [0]
            return

        for i in range(self.n):
            if i not in current_path and self.cost_matrix[current_path[-1]][i] != float('inf'):

                temp_bound = current_bound
                last_city = current_path[-1]
                temp_cost = current_cost + self.cost_matrix[last_city][i]

                row_min = min(
                    (self.cost_matrix[last_city][j] for j in range(self.n) if j not in current_path and j != last_city),
                    default=0
                )
                col_min = min(
                    (self.cost_matrix[j][i] for j in range(self.n) if j not in current_path and j != i),
                    default=0
                )

                temp_bound = temp_bound - row_min - col_min

                if temp_cost + temp_bound < self.best_cost:
                    current_path.append(i)
                    self.branch_and_bound(level + 1, current_path, temp_bound + self.cost_matrix[last_city][i], temp_cost)
                    current_path.pop()


