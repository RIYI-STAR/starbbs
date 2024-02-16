import os
from flask import *
import json as j
import time
import logging
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
methods = ['GET', 'POST']
app.secret_key = '1'
log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


@app.route('/', methods=methods)
def index():
    box_url_list = {
        'boot': {
            'box_1': 'images/index/boot/box_1.png',
            'box_2': 'images/index/boot/box_2.png',
            'box_3': 'images/index/boot/box_3.png'
        },
        'box_1': 'images/index/box_1.jpg',
        'box_2': 'images/index/box_2.jpg',
        'box_3': 'images/index/box_3.jpg'
    }
    return render_template('./index.html', box_url_list=box_url_list)


@app.route('/mine/', methods=methods)
def mine():
    if not session.get('user'):
        return redirect('/login/')
    else:
        with open(f'./static/config/users/{session["user"]}.json', 'r', encoding='u8') as fp:
            haven = j.loads(fp.read())
        if not haven['hava_read_board']:
            haven['hava_read_board'] = True
            with open(f'./static/config/users/{session["user"]}.json', 'w', encoding='u8') as fp:
                j.dump(haven, fp)
            return redirect('/board/')
        else:
            pass
        with open(f'./static/config/users/{session["user"]}.json', 'r', encoding='u8') as fp:
            session['information'] = j.loads(fp.read())
        path = './static/config/advices/'
        advice_list = os.listdir(path)
        advices_list = []
        for advice in advice_list:
            if advice.rsplit('.', 3)[1] == session['user']:
                with open(path+advice.rsplit('.', 3)[0]+'.'+session['user']+'.json', 'r', encoding='u8') as fp:
                    advices_list.insert(0, j.loads(fp.read()))
        return render_template('./mine.html', information=session['information'], advices_list=advices_list)


@app.route('/login/', methods=methods)
def login():
    if request.method == 'GET':
        return render_template('./login.html', mode='login')
    if request.method == 'POST':
        try:
            with open(f'./static/config/users/{request.form.get("user")}.json', 'r', encoding='u8') as fp:
                session['information'] = j.loads(fp.read())
            if session['information']['password'] == request.form.get('password'):
                session['user'] = request.form.get('user')
                return redirect('/mine/')
            else:
                return render_template('./login.html', mode='login', show='密码错误')
        except:
            return render_template('./login.html', mode='login', show='无此用户,请先注册')


@app.route('/region/', methods=methods)
def region():
    if request.method == "POST":
        try:
            open(f'./static/config/users/{request.form.get("user")}.json', 'r', encoding='u8')
            return render_template('./login.html', mode='region', show='该用户名已存在')
        except:
            session['information'] = {
                "birthday": "未设置",
                "introduction": "这个人很懒，还没有设置任何简介QWQ",
                "mw": "未设置",
                "name": request.form.get('name'),
                "password": request.form.get('password'),
                "phone-number": request.form.get('phone-number'),
                "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                "user": request.form.get('user'),
                "hava_read_board": False
            }
            with open(f'./static/config/users/{request.form.get("user")}.json', 'w+', encoding='u8') as fp:
                j.dump(session['information'], fp)
            path = './static/config/photos'
            with open(f'./{path}/system/user.png', 'rb') as fp:
                default = fp.read()
                print(default)
            with open(f'./{path}/user/{request.form.get("user")}.png', 'wb') as fp:
                fp.write(default)
            return redirect('/login/')

    return render_template('./login.html', mode='region')


@app.route('/logout/')
def logout():
    if not session.get('user'):
        return redirect('/login/')
    else:
        session.pop('user', None)
        session.pop('information', None)
        return redirect('/mine/')


@app.route('/information/', methods=methods)
def information():
    if not session.get('user'):
        return redirect('/login/')
    else:
        with open(f'./static/config/users/{session["user"]}.json', 'r', encoding='u8') as fp:
            haven = j.loads(fp.read())
        if not haven['hava_read_board']:
            haven['hava_read_board'] = True
            with open(f'./static/config/users/{session["user"]}.json', 'w', encoding='u8') as fp:
                j.dump(haven, fp)
            return redirect('/board/')
        else:
            pass
        error = False
        if request.method == 'POST':
            user_photo = request.files.get('user-photos-get')
            user_photo_name = secure_filename(user_photo.filename)
            if user_photo_name.rsplit(".", 1)[1] in ['png', 'jpg']:
                user_photo.save(f'./static/config/photos/user/{session["user"]}.png')
            else:
                error = True

        with open(f'./static/config/users/{session["user"]}.json', 'r', encoding='u8') as fp:
            session['information'] = j.loads(fp.read())
        return render_template('./information.html', information=session['information'], error=error)


@app.route('/editor/', methods=methods)
def editor():
    k = request.args.get('k')
    if not session.get('user'):
        return redirect('/login/')
    else:
        if request.method == 'POST':
            session['information'][f'{k}'] = request.form.get('value')
            with open(f'./static/config/users/{session["user"]}.json', 'w', encoding='u8') as fp:
                j.dump(session['information'], fp)
            return redirect('/mine/')
        return render_template('./editor.html', k=k)


@app.route('/advices/', methods=methods)
def advices():
    if not session.get('user'):
        return redirect('/login/')
    else:
        if request.method == "POST":
            advice = str(request.form.get('value'))
            name = time.strftime('%m-%d %H%M%S.', time.localtime()) + session['user']
            with open(f'./static/config/advices/{name}.json', 'w', encoding='u8') as fp:
                j.dump({
                    'message': advice,
                    'answer': '',
                    'user': session['user'],
                    'worker': ''
                }, fp)
            return redirect('/mine/')
        return render_template('./editor.html', k='advice')


@app.route('/usersetting/', methods=methods)
def usersetting():
    if not session.get('user'):
        return redirect('/login/')
    else:
        with open(f'./static/config/users/{session["user"]}.json', 'r', encoding='u8') as fp:
            session['information'] = j.loads(fp.read())
        return render_template('./usersetting.html', information=session['information'])


@app.route('/about/')
def about():
    return render_template('./about.html')


@app.route('/freehelp/')
def freehelp():
    return render_template('./freehelp.html')


@app.route('/conversation/', methods=methods)
def conversation():
    if request.method == 'POST':
        if not session.get('user'):
            return redirect('/login/')
        else:
            date = time.strftime('%Y-%m-%d', time.localtime())
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            session['news_list'].insert(0, {
                "user": session['user'],
                "name": session['information']['name'],
                "message": request.form.get('message'),
                "time": now
            })
            with open(f'./static/config/public-news/{date}.json', 'w', encoding='u8') as fp:
                j.dump(session['news_list'], fp)
    return render_template('./conversation.html')


@app.route('/public-news/', methods=methods)
def public_news():
    if request.method == "POST":
        return session['news_list']
    date = time.strftime('%Y-%m-%d', time.localtime())
    try:
        with open(f'./static/config/public-news/{date}.json', 'r', encoding='u8') as fp:
            session['news_list'] = j.load(fp)
    except:
        with open(f'./static/config/public-news/{date}.json', 'w', encoding='u8') as fp:
            session['news_list'] = [{
                "user": "Starbot",
                "name": "欢迎词",
                "message": "大家好，又是新的一天，欢迎大家的到来",
                "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }]
            json.dump(session['news_list'], fp)
    return render_template('./public-news.html', news_list=session['news_list'])


@app.route('/bbs/')
def bbs():
    with open(f'./static/config/users/{session["user"]}.json', 'r', encoding='u8') as fp:
        haven = j.loads(fp.read())
    if not haven['hava_read_board']:
        haven['hava_read_board'] = True
        with open(f'./static/config/users/{session["user"]}.json', 'w', encoding='u8') as fp:
            j.dump(haven, fp)
        return redirect('/board/')
    else:
        pass
    return render_template('./bbs.html')

@app.route('/user/', methods=methods)
def user():
    user = request.args.get('user')
    with open(f'./static/config/users/{user}.json', 'r', encoding='u8') as fp:
        information = j.loads(fp.read())
    return render_template('user.html', information=information)

@app.route('/board/')
def board():
    with open('./static/config/board/board.json', 'r', encoding='u8') as fp:
        board_text = j.loads(fp.read())
    return render_template('./board.html', board_text=board_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
