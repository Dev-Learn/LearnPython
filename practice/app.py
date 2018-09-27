from flask import Flask
from flask import render_template
import json
import os
import glob
import codecs

app = Flask(__name__)


@app.route('/')
def home():
    dir_name = '07-2018'
    if not os.path.isdir(dir_name):
        return 'Không tồn tại thư mục chứa dữ liệu'

    data = []
    for item in glob.glob(dir_name + '/' + '*.json'):
        f = codecs.open(item, 'r', encoding='utf-8')
        data.append(json.load(f))
    return render_template('home_page.html', articles=data)


@app.route('/article/<detail_id>')
def detail(detail_id):
    dir_name = '07-2018'
    fn = '%s/%s.json' %(dir_name, detail_id)
    print(fn)
    print(os.path.isfile(fn))
    if not os.path.isfile(fn):
        return 'Không tồn tại tập tin %s.json' % detail_id

    f = codecs.open(fn, 'r', encoding='utf-8')
    data = json.load(f)

    return render_template('detail_page.html', article=data)
