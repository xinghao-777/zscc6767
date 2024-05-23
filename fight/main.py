import pygame as pg
import control_system
if __name__ == "__main__":
    con = control_system.Control()
    con.run()

# 卡牌列表
# my_cards = [
#     Cards("golder", 10, 10, 0, 5, "A","images/golder.png"),
#     Cards("basic_arrow", 20, 10, 2, 0, "B", "images/basic_arrow.png"),
#     # ... 添加其他卡牌
# ]
#



# 退出pygame，循坏外执行


'''def get_neighbors(grid, pos):
    neighbors = []
    dx, dy = pos
    for nx, ny in [(dx - 1, dy), (dx + 1, dy), (dx - 1, dy - 1), (dx + 1, dy - 1), (dx, dy - 1), (dx, dy + 1)]:
        if (nx, ny) in grid:
            neighbors.append((nx, ny))
    return neighbors

# Dijkstra算法
def dijkstra(grid, start, end):
    distances = {pos: float('infinity') for pos in grid}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_pos = heapq.heappop(queue)

        if current_distance > distances[current_pos]:
            continue

        for neighbor in get_neighbors(grid, current_pos):
            distance = current_distance + 1  # 假设每次移动一个六边形格的距离为1  
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

        if current_pos == end:
            break

            # 构造最短路径（如果需要的话）
    path = []
    current = end
    while current != start:
        path.append(current)
        current = min(get_neighbors(grid, current), key=lambda x: distances.get(x, float('infinity')))
    path.append(start)
    path.reverse()

    return distances[end], path

# 示例地图（使用坐标表示六边形，这里仅示意）
# 注意：实际的六边形网格可能需要一个更复杂的模型来准确表示其连接性  
grid = {
    (0, 0): None,  # 假设这是X的位置  
    (2, 2): None,  # 假设这是A的位置  
    # 其他六边形...  
}

# 设置X和A的位置  
X = (0, 0)
A = (2, 2)

# 调用Dijkstra算法找到最短路径  
distance, path = dijkstra(grid, A, X)

print(f"The shortest distance from A to X is: {distance}")
print(f"The path is: {path}")'''