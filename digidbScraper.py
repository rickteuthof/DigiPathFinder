import json
import numpy as np
import pandas as pd
import requests


def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1,
                     length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}"
               ).format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    if iteration == total:
        print()


baseurl = 'http://digidb.io/digimon-search/?request='
database = {}

for i in range(1, 342):
    response = requests.get(baseurl+str(i))
    dfs = pd.read_html(response.text)

    # Get Name
    digimon = dfs[0].to_numpy()[0][1][5::]
    digimon = strip_end(digimon, 'Baby')
    digimon = strip_end(digimon, 'In-Training')
    digimon = strip_end(digimon, 'Rookie')
    digimon = strip_end(digimon, 'Champion')
    digimon = strip_end(digimon, 'Ultimate')
    digimon = strip_end(digimon, 'Mega')
    digimon = strip_end(digimon, 'Ultra')
    digimon = strip_end(digimon, 'Armor')
    digimon = strip_end(digimon, 'None')
    database[digimon] = {}

    # Get Prevs
    prev_list = dfs[1].to_numpy()[1::]
    database[digimon]['prev'] = []
    if not prev_list[0][0] is np.nan:
        for p in prev_list[0][0].split(' '):
            database[digimon]['prev'] += [p]

    # Get Nexts
    next_list = dfs[2].to_numpy()[1::]
    database[digimon]['next'] = {}
    if not next_list[0][0] is np.nan:
        for n in next_list:
            database[digimon]['next'][n[0]] = {}
            database[digimon]['next'][n[0]]['level'] = n[1][7::]
            require_db = {}
            requires = n[2][10::].split(',')
            for require in requires:
                if len(require.split(':')) == 1:
                    require_db['special'] = require.strip()
                else:
                    require_db[require.split(':')[0].strip()] = \
                        require.split(':')[1].strip()
            database[digimon]['next'][n[0]]['requires'] = require_db

    # Get Skills
    skills = dfs[3].to_numpy()[1::]
    database[digimon]['skills'] = {}
    for skill in skills:
        if skill[6] != 'Yes':
            continue
        database[digimon]['skills'][skill[1]] = skill[0]

    printProgressBar(i + 1, 342, prefix='Progress:',
                     suffix='Complete', length=50)

with open('database.json', 'w') as fp:
    json.dump(database, fp)
