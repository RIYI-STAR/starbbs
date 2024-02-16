import json
import os

path = './static/config/advices/'
files = os.listdir(path)

worker = input('你的名称：')

for file in files:
    with open(path+file, 'r', encoding='u8') as fp:
        advices = json.loads(fp.read())
    if advices['answer'] == '':
        print('\n建议：'+advices['message'])
        print('建议者：'+advices['user'])
        answer = input('回复：')
        with open(path+file, 'w', encoding='u8') as fp:
            advices['answer'] = answer
            advices['worker'] = worker
            json.dump(advices, fp)
    else:
        pass