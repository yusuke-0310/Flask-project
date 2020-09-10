from flask import Flask, render_template, request, redirect, url_for

import json

import sqlite3

#アプリオブジェクトの作成
app = Flask(__name__)

#ルーティング
@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/hive')
def hive():
    return render_template('index.html')

#変数を渡すURL
@app.route('/var')
def var():
    message = 'こんにちは'
    return render_template('var.html', message=message)

#For文を利用するURL
@app.route('/greeting')
def greeting():
    message_list = ['おはよう', 'こんにちは', 'こんばんは']
    return render_template('greeting.html', message_list=message_list)


@app.route('/fizzbuzz')
def fizzbuzz():
    result = []
    for i in range(1, 100):
        if i % 15 == 0:
            result.append('FIZZBUZZ')
        elif i % 3 == 0:
            result.append('FIZZ')
        elif i % 5 == 0:
            result.append('BUZZ')
        else:
            result.append(i)
    return render_template('fizzbuzz.html', result=result)

@app.route('/get')
def get():
    name = request.args.get('name')
    return render_template('get.html', title='Flask GET request', name=name)

@app.route('/getnumber')
def getnumber():
    n = int(request.args.get('number'))
    for p in range (2, n):
        if n % p == 0:
            number = '素数ではありません'
            break
        else:
            number = '素数です'
    return render_template('getnumber.html', title='Flask GET request', number=number)

#def get_profile():
    #JSONファイルの読み込み
    #file_json = "data/profile.json"
    #prof = open(file_json, encoding='utf-8')
    #json_str = prof.read()
    #prof.close()

    #JSONから辞書型に変換
    #prof_dict = json.loads(json_str)
    #return prof_dict

def get_number():
    file_json = "data/number.json"
    num = open(file_json, encoding='utf-8')
    json_int = num.read()
    num.close()

    num_dict = json.loads(json_int)
    return num_dict

#def update_profile(prof):
    #f = open('data/profile.json', 'w')
    #json.dump(prof, f)
    #f.close()

def update_number(num):
    f = open('data/number.json', 'w')
    json.dump(num, f)
    f.close()

def get_profile():
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    prof_list=[]
    for i in c.execute('select * from persons'):
        prof_list+=[{'id':i[0],'name':i[1],'age':i[2],'sex':i[3]}]
    conn.commit()
    conn.close()
    return prof_list

def update_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('update persons set name=?,age=?,sex=? WHERE id=?',(prof['name'],prof['age'],prof['sex'],prof['id']))
    conn.commit()
    conn.close()

def add_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    print(prof["id"],prof["name"],prof["age"],prof["sex"])
    c.execute('insert into persons(id,name,age,sex) values(?,?,?,?)', (prof["id"],prof["name"],prof["age"],prof["sex"]))
    conn.commit()
    conn.close()

def destroy_profile(id):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('delete from persons where id=?',str(id))
    #return str(id)
    conn.commit()
    conn.close()
    
@app.route('/profile')
def profile():
    prof_dict = get_profile()
    return render_template('profile.html', title='json', user=prof_dict)

@app.route('/number')
def number():
    num_dict = get_number()
    return render_template('number.html', title='json', user=num_dict)

@app.route('/edit/<int:id>')
def edit(id):
    prof_list = get_profile()
    for i in prof_list:
        if i['id'] == id:
            prof_dict = i
    return render_template('edit.html', title='sql', user=prof_dict)

@app.route('/editnumber')
def editnumber():
    num_dict = get_number()
    return render_template('editnumber.html', title='json', user=num_dict)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    prof_list = get_profile()
    for i in prof_list:
        if i['id'] == id:
            prof_dict = i
    #prof_dictの値を変更
    prof_dict['name'] = request.form['name']
    prof_dict['age'] = request.form['age']
    prof_dict['sex'] = request.form['sex']
    #return prof_dict['name']
    update_profile(prof_dict)

    return redirect(url_for('profile'))

@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        prof_dict={'id':"",'name':"", 'age':"", 'sex':""}
        prof_dict['id'] = request.form['id']
        prof_dict['name'] = request.form['name']
        prof_dict['age'] = request.form['age']
        prof_dict['sex'] = request.form['sex']
        add_profile(prof_dict)

        return redirect(url_for('profile'))

    return render_template('add.html')

@app.route('/insert/', methods=['POST'])
def insert(id):
    prof_dict={'id':"",'name':"", 'age':"",'sex':""}
    prof_dict['id'] = request.form['id']
    prof_dict['name'] = request.form['name']
    prof_dict['age'] = request.form['age']
    prof_dict['sex'] = request.form['sex']
    add_profile(prof_dict)

    return redirect(url_for('profile'))

@app.route('/destroy/<int:id>')
def destroy(id):
    #prof_list = get_profile()
    #prof_dict = prof_list[id-1]
    
    destroy_profile(id)
    
    return redirect(url_for('profile'))
    #return str(id)

@app.route('/updatenumber', methods=['POST'])
def updatenumber():
    num_dict = get_number()
    num_dict['number'] = request.form['number']

    update_number(num_dict)

    return redirect (url_for("number"))

if __name__ == "__main__":
    app.run(debug=True)