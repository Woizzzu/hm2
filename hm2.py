import heapq

def dijkstra(graph, start):
    # Инициализация расстояний
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0

    # Для восстановления пути
    previous = {vertex: None for vertex in graph}

    # Очередь с приоритетом (расстояние, вершина)
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Если нашли более длинный путь — пропускаем
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            # Если нашли более короткий путь
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous


def get_path(previous, start, end):
    path = []
    current = end

    while current:
        path.append(current)
        current = previous[current]

    path.reverse()
    
    return path if path[0] == start else []


# Граф
graph = {
    'A': {'B': 7, 'C': 9, 'F': 14},
    'B': {'C': 10, 'D': 15},
    'C': {'D': 11, 'F': 2},
    'D': {'E': 6},
    'E': {'F': 9},
    'F': {}
}

# Запуск
distances, previous = dijkstra(graph, 'A')
path = get_path(previous, 'A', 'E')

print("Кратчайший путь:", "".join(path))
print("Длина пути:", distances['E'])