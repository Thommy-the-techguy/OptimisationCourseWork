import pygame as pg
from heapq import *


def get_circle(x, y):
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


def get_neighbours(x, y):
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]


# def get_click_mouse_pos():
#     x, y = pg.mouse.get_pos()
#     grid_x, grid_y = x // TILE, y // TILE
#     pg.draw.circle(sc, pg.Color('red'), *get_circle(grid_x, grid_y))
#     click = pg.mouse.get_pressed()
#     return (grid_x, grid_y) if click[0] else False


def get_arrow_key_pos():
    global x, y
    events = pg.event.get()
    keydown = False
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                x -= 50
                keydown = True
            if event.key == pg.K_RIGHT:
                x += 50
                keydown = True
            if event.key == pg.K_DOWN:
                y += 50
                keydown = True
            if event.key == pg.K_UP:
                y -= 50
                keydown = True
        if keydown:
            grid_x, grid_y = x // TILE, y // TILE
            pg.draw.circle(sc, pg.Color('red'), (x, y), TILE // 4)
            # print(f"x: {x}")
            # print(f"y: {y}")
            # print(f"grid_x: {grid_x}")
            # print(f"grid_y: {grid_y}")
            return grid_x, grid_y
    return False


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dijkstra(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited


def computer_move(path_segment):
    global start
    start = path_segment


cols, rows = 23, 13
TILE = 50

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# set grid
# grid = ['22222222222222222222212',
#         '22222292222911112244412',
#         '22444422211112911444412',
#         '24444444212777771444912',
#         '24444444219777771244112',
#         '92444444212777791192144',
#         '22229444212777779111144',
#         '11111112212777772771122',
#         '27722211112777772771244',
#         '27722777712222772221244',
#         '22292777711144429221244',
#         '22922777222144422211944',
#         '22222777229111111119222']
# underground_dungeon grid
grid = ['22222222222222222222222',
        '24444224221111111112482',
        '24994222221222222212482',
        '24994221111228299212222',
        '24444221771288824444111',
        '22222221771288824774122',
        '11111111771229924774122',
        '22222177771222224774122',
        '22992177771221114774122',
        '28492122221222224774122',
        '28492111111222224444122',
        '22299222221222221111122',
        '22222222221111111222222']

grid = [[int(char) for char in string] for string in grid]
# adjacency dict
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)

start = (0, 7)
goal = (22, 7)
queue = []
heappush(queue, (0, start))
visited = {start: None}
blues = []

bg = pg.image.load('img/underground_dungeon.png').convert()
bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))
x, y = 1122, 362
while True:
    # fill screen
    sc.blit(bg, (0, 0))

    # get path to mouse click
    # mouse_pos = get_click_mouse_pos()
    mouse_pos = get_arrow_key_pos()
    if mouse_pos:
        visited = dijkstra(start, mouse_pos, graph)
        goal = mouse_pos

    # draw path
    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        if path_segment != start and path_segment != visited.get(start):
            pg.draw.circle(sc, pg.Color('blue'), *get_circle(*path_segment))
        # print(path_segment)
        blues.append(path_segment)
        path_segment = visited[path_segment]
    # print("\n")
    # print(blues)
    # print(blues[len(blues) - 1])
    # print("\n\n")
    pg.draw.circle(sc, pg.Color('green'), *get_circle(*start))
    pg.draw.circle(sc, pg.Color('magenta'), *get_circle(*path_head))
    if len(blues) > 1:
        computer_move(blues[-2])

    if mouse_pos and start == goal:
        break

    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(30)

input()