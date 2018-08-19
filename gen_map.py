from cal_Probability import *
from random import choice
from random import randint
import networkx as nx
from sys import maxsize
import matplotlib.pyplot as plt
import numpy as np
import util
import csv

nodes = [i for i in range(1,loc_nums + 1)]
# path = np.array([loc_nums + 1,loc_nums + 1], dtype=tuple)
out = {}
delta = {}
def gen_node_list() -> list:
    node_list = []
    count = np.zeros([loc_nums + 1,1])
    check = np.zeros([loc_nums + 1, loc_nums + 1])
    for i in range(len(nodes)):
        from_node = nodes[i]
        j = randint(1,4)
        for k in range(j):
            to_node = 0
            for m in range(len(nodes)):
                to_node = nodes[m]
                if check[from_node][to_node] == 0 and count[to_node][0] <= 4 and from_node != to_node:
                    break
            if to_node == 0:
                break
            tuple_temp = (from_node, to_node, randint(1,20))
            check[from_node][to_node] = 1
            check[to_node][from_node] = 1
            count[to_node][0] += 1
            count[from_node][0] += 1
            node_list.append(tuple_temp)
    np.savetxt(r'data\node_list.csv', node_list, delimiter=',', fmt = '%d')
    gen_graph(node_list)
    return node_list

def gen_map():
    node_map = [[maxsize for val in range(len(nodes))] for val in range(len(nodes))]
    path_map = [[0 for val in range(len(nodes))] for val in range(len(nodes))]
    return node_map, path_map

def set_Floyd_Path():
    global delta,out
    node_map, path_map = gen_map()
    node_list = list(csv.reader(open(r'data\node_list.csv', 'r')))
    for i in range(len(node_list)):
        node_list[i] = tuple(list(map(int,node_list[i])))
    for i in range(len(nodes)):
        node_map[i][i] = 0
    for i in nodes:
        out[i] = []
        delta[(i,i)] = 0
    for x,y,val in node_list:
        out[x].append(y)
        out[y].append(x)
        delta[(x,y)] = delta[(y,x)] = val / util.average_speed
        node_map[nodes.index(x)][nodes.index(y)] = node_map[nodes.index(y)][nodes.index(x)] = val
        path_map[nodes.index(x)][nodes.index(y)] = nodes.index(y)
        path_map[nodes.index(y)][nodes.index(x)] = nodes.index(x)
    floyd_path = util.Floyd_Path(nodes, node_map, path_map)
    return floyd_path

def gen_graph(node_list: list):
    G = nx.Graph()
    G.add_weighted_edges_from(node_list)
    nx.draw_spring(G, with_labels=True,font_size = 10, node_size = 16)
    plt.show()
    return

