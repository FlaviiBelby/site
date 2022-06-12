import psycopg2 as p
from flask import Flask
from flask import redirect, render_template, request

def check(string):
    res = 0
    res += (' ' in string)
    res += ('&' in string)
    res += ('?' in string)
    res += ('!' in string)
    res += ('@' in string)
    res += (':' in string)
    return res


def add(model, seria, howmuch):
    con = p.connect(dbname='infobook', user='postgres',
                    password='#password#', host='localhost')

    cr = con.cursor()

    cr.execute(f"INSERT INTO info(model, seria, howmuch) VALUES ('{model}', '{seria}', {howmuch});")

    con.commit()
    con.close()


def get_data():
    con = p.connect(dbname='infobook', user='postgres',
                    password='#password#', host='localhost')

    cr = con.cursor()

    cr.execute("SELECT * FROM info;")
    data = cr.fetchall()

    con.commit()
    con.close()

    all_data = []
    for record in data:
        all_data.append({'nom': record[0], 'model': record[1], 'seria': record[2], 'howmuch': record[3]})
    return all_data


app = Flask(__name__)


@app.route('/')
def home():
    return redirect('/info/')


@app.route('/info/', methods=['post', 'get'])
def users():
    model, seria, howmuch = '', '', 0
    message = ''
    if request.method == 'POST':
        model = request.form.get('model')
        seria = request.form.get('seria')
        howmuch = request.form.get('howmuch')

    if (model != '') & (seria != ''):
        if (check(model) == 0) & (check(seria) == 0):
            if howmuch != None:
                if (int(howmuch) >= 0):
                    add(model, seria, howmuch)
                else:
                    message = 'Wrong quant format'
            else:
                add(model, seria, 0)
        else:
            message = 'Wrong data format'
    data = []
    for record in get_data():
        data.append(f"{record['model']} {record['seria']} {record['howmuch']}")
    return render_template("index.html", data=data, message=message)

if __name__ == '__main__':
    app.run(debug=True)
