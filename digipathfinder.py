import json

import matplotlib.pyplot as plt
import networkx as nx

G = nx.MultiDiGraph()

with open('database.json') as json_file:
    database = json.load(json_file)

for cur_name in database.keys():
    for prev_name in database[cur_name]['prev']:
        G.add_edge(cur_name, prev_name, direction='down')

    for next_name in database[cur_name]['next'].keys():
        G.add_edge(cur_name, next_name, direction='up')


def get_path(digimon1, digimon2):
    path = nx.shortest_path(G, digimon1, digimon2)
    print(path[0])
    for i in range(len(path) - 1):
        direction = G.get_edge_data(path[i], path[i+1])[0]['direction']
        print(direction)
        print(path[i+1])


get_path('Clockmon', 'Angewomon')
# pos = nx.spring_layout(G)
# nx.draw(G, pos)
# labels = nx.draw_networkx_labels(G, pos)
# plt.show()
