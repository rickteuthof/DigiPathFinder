import json

with open('database.json') as json_file:
    database = json.load(json_file)

skill_database = {}

for digimon in database:
    for skill in database[digimon]['skills']:
        if skill not in skill_database:
            skill_database[skill] = []
        skill_database[skill].append(
            (digimon, database[digimon]['skills'][skill]))

for skill in skill_database:
    skill_database[skill].sort(key=lambda x: x[1])

with open('skill_database.json', 'w') as fp:
    json.dump(skill_database, fp)