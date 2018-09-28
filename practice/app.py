from flask import Flask
from flask import render_template
import json
import os
import glob
import codecs

"""
    flask --help
    flask run --help
"""

app = Flask(__name__)


@app.route('/')
def home():
    data = []
    # Lấy tất cả folder trong thư mục practice
    for child in os.listdir('.'):
        # Kiểm tra có phải folder và tên có chứa '-'
        if os.path.isdir(child) and '-' in child:
            data.append(child)
    return render_template('home_page.html', folders=data)

@app.route('/day/<day_id>')
def folder(day_id):
    dir_name = day_id
    if not os.path.isdir(dir_name):
        return 'Không tồn tại thư mục chứa dữ liệu'

    data = []
    for item in glob.glob(dir_name + '/' + '*.json'):
        f = codecs.open(item, 'r', encoding='utf-8')
        data.append(json.load(f))
    return render_template('folder_page.html', articles=data,title = day_id)


@app.route('/article/<day_id>/<detail_id>')
def detail(day_id,detail_id):
    dir_name = day_id
    fn = '%s/%s.json' %(dir_name, detail_id)
    print(fn)
    print(os.path.isfile(fn))
    if not os.path.isfile(fn):
        return 'Không tồn tại tập tin %s.json' % detail_id

    f = codecs.open(fn, 'r', encoding='utf-8')
    data = json.load(f)

    return render_template('detail_page.html', article=data)
