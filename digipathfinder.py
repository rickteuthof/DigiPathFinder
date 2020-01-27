import json

import networkx as nx

G = nx.MultiDiGraph()

with open('digiData.json') as json_file:
    digimon = json.load(json_file)


for i in digimon.keys():
    for p in digimon[i]['neighBours']['prev']:
        G.add_edge(digimon[i]['name'], digimon[p]['name'], direction='down')

    for n in digimon[i]['neighBours']['next']:
        G.add_edge(digimon[i]['name'], digimon[n]['name'], direction='up')

path = nx.shortest_path(G, 'LadyDevimon', 'Angewomon')

print(path[0])
for i in range(len(path) - 1):
    direction = G.get_edge_data(path[i], path[i+1])[0]['direction']
    print(direction)
    print(path[i+1])

# pos = nx.kamada_kawai_layout(G)
# nx.draw(G, pos)
# labels = nx.draw_networkx_labels(G, pos)
# plt.show()
