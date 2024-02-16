import os
from tqdm import tqdm

names = os.listdir('./static/config/users')
path = './static/config/photos'
for name in tqdm(names):
    with open(f'./{path}/system/user.png', 'rb') as fp:
        default = fp.read()
    with open(f'./{path}/user/{name.split(".")[-2]}.png', 'wb') as fp:
        fp.write(default)




