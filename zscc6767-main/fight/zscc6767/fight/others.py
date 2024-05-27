def calculate_hex_rc(row, col):  # 用于计算给定行和列索引的六边形的以中心点为（0，0）分布的坐标。
    r = row - (13 + 1) // 2
    c = ((col - 1 / 2) - ((13 - 1) // 2 + row) / 2) * 2
    return r, c
print(calculate_hex_rc(7,7))