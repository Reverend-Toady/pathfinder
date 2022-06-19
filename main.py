from __future__ import annotations
from typing import Optional, Tuple, List
from dataclasses import dataclass
from time import sleep
from GRID_STATES import GRID3 as GRID
import os


NODE_STATES = {
    "traversed" : "🟥",
    "idle"      : "⬜",
    "neighbour" : "🟩",
    "block"     : "⬛",
    "start"     : "🟨",
    "end"       : "🟦",
}

SIZE = 35 


@dataclass()
class Node:
    g_cost: float # distance from start node 
    h_cost: float # distance from end node 
    f_cost: float # sum of h_cost and g_cost
    node_state: str
    position: Tuple[int, int]
    parent: Optional[Node] 

def distance_formula(postion1: Tuple[int, int], postion2: Tuple[int, int]) -> float:
    x1, y1 = postion1
    x2, y2 = postion2 
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

def clear_screen() -> None:
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def create_grid(grid: List[List[str]]) -> Tuple:
    start_node = end_node = None
    main_grid = []
    for y, row in enumerate(grid):
        main_row = []
        for x, item in enumerate(row):
            node = Node(
                        g_cost=0, 
                        h_cost=0, 
                        f_cost=0, 
                        node_state="", 
                        position= (x, y),
                        parent= None
                    )
            if item == "": node.node_state = "idle"
            elif item == "1": node.node_state = "block"
            elif item == "x": 
                node.node_state = "end"
                end_node = node 
            elif item == "o": 
                node.node_state = "start"
                start_node = node 
            
            main_row.append(node)
        main_grid.append(main_row)
    
    return (main_grid, start_node, end_node)

def print_grid(grid: List[List[Node]]) -> None:
    for row in grid:
        for item in row:
            print(NODE_STATES[item.node_state], end= "")
        print()
 
def main() -> None:
    grid, start_node, end_node = create_grid(GRID)
    open_nodes = [start_node]
    closed_nodes = []
    path_node = None

    running = True
    while running:
        temp_sorted_nodes = sorted(open_nodes, key= lambda node: node.f_cost)
        sorted_nodes = []
        for node in temp_sorted_nodes:
            if node.f_cost == temp_sorted_nodes[0].f_cost:
                sorted_nodes.append(node)
        
        current_node = sorted(sorted_nodes, key= lambda node: node.h_cost)[0]
        current_node.node_state = "traversed"
        open_nodes.pop(open_nodes.index(current_node))
        closed_nodes.append(current_node)

        if current_node.position == end_node.position:
            path_node = current_node
            running = False

        node_x, node_y = current_node.position
        top_neighbour     = grid[node_y - 1][node_x    ]
        bottom_neighbour  = grid[node_y + 1][node_x    ]
        left_neighbour    = grid[node_y    ][node_x - 1]
        right_neighbour   = grid[node_y    ][node_x + 1]

        neighbour_list = [top_neighbour, left_neighbour, bottom_neighbour, right_neighbour]
        for node in neighbour_list:
            if node in closed_nodes or node.node_state == "block":
                continue

            new_g_cost = distance_formula(node.position, start_node.position)
            if node.g_cost == 0:
                node.g_cost = new_g_cost
    
            if new_g_cost < node.g_cost or node not in open_nodes:
                if new_g_cost < node.g_cost:
                    node.g_cost = new_g_cost

                node.h_cost = distance_formula(node.position, end_node.position)
                node.f_cost = node.g_cost + node.h_cost
                node.node_state = "neighbour"
                node.parent = current_node

                if node not in open_nodes:
                    open_nodes.append(node)
            
            node_x, node_y = node.position 
            grid[node_y][node_x] = node

        sleep(0.01)
        clear_screen()
        print_grid(grid)
    clear_screen()
    
    if path_node:
        while path_node.parent is not None:
            x, y = path_node.position
            node = grid[y][x]
            node.node_state = "end"
            grid[y][x] = node
            path_node = path_node.parent
    print_grid(grid) 

if __name__ == "__main__":
    main()
