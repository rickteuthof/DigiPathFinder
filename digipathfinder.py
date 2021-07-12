import json

import matplotlib.pyplot as plt
import networkx as nx

G = nx.MultiDiGraph()

with open('database.json') as json_file:
    database = json.load(json_file)

for digimon in database:
    for prev_digimon in database[digimon]['prev']:
        G.add_edge(digimon, prev_digimon, direction='down', weight=0)

    for next_digimon in database[digimon]['next']:
        weight = int(database[digimon]['next'][next_digimon]['Level'])
        G.add_edge(digimon, next_digimon, direction='up', weight=weight)

with open('skill_database.json') as json_file:
    skill_database = json.load(json_file)


def get_path(start, end, withskills=[]):
    nodes = [start]
    for skill in withskills:
        nodes.append(skill_database[skill][0][0])
    nodes.append(end)
    for start, end, skill in zip(nodes[:-1], nodes[1:], withskills+['']):
        path = nx.dijkstra_path(G, start, end)
        for i in range(len(path) - 1):
            direction = G.get_edge_data(path[i], path[i+1])[0]['direction']
            print("%s -> %s -> %s" % (path[i], direction, path[i+1]))
        if skill:
            print("Get skill %s" % skill)


get_path('LadyDevimon', 'Angewomon', withskills=["Gaia Element I"])
# pos = nx.spring_layout(G)
# nx.draw(G, pos)
# labels = nx.draw_networkx_labels(G, pos)
# plt.show()
