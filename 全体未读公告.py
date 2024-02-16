import os
import json
from tqdm import tqdm

path = './static/config/users/'
files = os.listdir(path)
for file in tqdm(files):
    with open(path + file, 'r', encoding='u8') as fp:
        j = json.loads(fp.read())
    j['hava_read_board'] = False
    with open(path + file, 'w', encoding='u8') as fp:
        json.dump(j, fp)
print('完成')