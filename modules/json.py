import json

def load(filename):
#load file, or create file
    location = f'./modules/files/{filename}.json'
    try:
        a_file = open(location, "r")
        data = json.load(a_file)
        a_file.close()
    except:
        print('file doesnt exist, created empty file')
        data = {}
        a_file = open(location, "w")
        json.dump(data, a_file)
        a_file.close()
    return data

def edit(filename, data):
    location = f'./modules/files/{filename}.json'
    a_file = open(f'{location}', "w")
    json.dump(data, a_file)
    a_file.close()