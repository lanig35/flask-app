from faker import Faker
import json

datagen = Faker ('fr_FR')

dataset = []
for i in range (1,5):
    item = {
     'name': datagen.company(),
     'city': datagen.city(),
     'phone': datagen.phone_number()
    }
    dataset.append (item)

with open ('json.txt', 'w') as f:
    json.dump (dataset, f)

print json.dumps (dataset)



