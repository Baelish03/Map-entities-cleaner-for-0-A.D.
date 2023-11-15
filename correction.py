import os


def map_info():
    with open(file="map_info.txt", mode='r') as f:
        all_infos = f.readlines()
    all_infos = all_infos[2:]
    all_infos[0] = all_infos[0].replace("<.XML FILE PATH:>", "").replace("\n", "")
    all_infos[1] = all_infos[1].replace("<.XML FILE NAME:>", "").replace("\n", "")
    all_infos[2] = all_infos[2].replace("<MAP SIZE(LOWCASE):>", "").replace("\n", "")
    return all_infos


def inp():
    with open(FILE, 'r') as f:
        all_file = f.read()
    all_list = all_file.split('Entities')
    entities = all_list[1]
    entities_list = entities.split('</Entity>')
    entities_list = entities_list[:-1]
    entities_matrix = []
    for i in range(len(entities_list)):
        entities_matrix.append(entities_list[i].split('\n'))
    for i in entities_matrix:
        i[4] = i[4].replace('\t\t\t<Position x=\"', '').replace('\"/>', '').split('\" z=\"')
        i[4][0] = float(i[4][0])
        i[4][1] = float(i[4][1])
    # print(entities_matrix[-1])
    return entities_matrix, [all_list[0], all_list[2]]


def map_data():
    if MAP_SIZE == 'tiny':  # square side = 512     border = 16
        center = 256
        radius = 240
    elif MAP_SIZE == 'small':  # square side = 768     border = 16
        center = 384
        radius = 368
    elif MAP_SIZE == 'normal':  # square side = 1024     border = 16
        center = 512
        radius = 496
    elif MAP_SIZE == 'medium':  # square side = 1280     border = 16
        center = 640
        radius = 624
    elif MAP_SIZE == 'large':  # square side = 1536     border = 16
        center = 768
        radius = 752
    elif MAP_SIZE == 'very large':  # square side = 1792     border = 16
        center = 896
        radius = 880
    elif MAP_SIZE == 'giant':  # square side = 2048     border = 16
        center = 1024
        radius = 1008
    return [center, radius]


def elim(matrix, data):
    clean_matrix = []
    for i in matrix:
        if ((i[4][0]-data[0])**2+(i[4][1]-data[0])**2)**0.5 < data[1]:
            clean_matrix.append(i)
    # print(clean_matrix)
    return clean_matrix


def recompose(matrix, ous):
    for i in matrix:
        i[4] = '\t\t\t<Position x=\"' + str(i[4][0]) + '\" z=\"' + str(i[4][1]) + '\"/>'

    entities_list = []
    for i in matrix:
        p = (i[1] + '\n' + i[2] + '\n' + i[3] + '\n'
             + i[4] + '\n' + i[5] + '\n' + i[6] + '\n' + i[7] + '</Entity>' + '\n')
        entities_list.append(p)
    # print(entities_list[0])

    entities_str = ''
    entities_str = entities_str.join(entities_list)
    # print(entities_str)

    all_file_str = ous[0] + 'Entities>\n' + entities_str + '\t</Entities' + ous[1]
    # print(all_file_str)
    return all_file_str


def print_file(text):
    with open(FILE, 'w') as f:
        f.write(text)
        f.close()


if __name__ == '__main__':
    os.chdir(map_info()[0])
    FILE = map_info()[1]
    MAP_SIZE = map_info()[2]
    DATA = map_data()
    EN_MATRIX = inp()[0]  # ENTITIES MATRIX
    OLD_USEFUL_STUFF = inp()[1]
    CLEAN_MATRIX = elim(EN_MATRIX, DATA)
    CORRECT_TEXT = recompose(CLEAN_MATRIX, OLD_USEFUL_STUFF)
    print_file(CORRECT_TEXT)
