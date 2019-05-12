from flask import Flask, render_template, request,send_from_directory
import os
from xml.dom import minidom
import xlsxwriter

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    global excelFile
    target = os.path.join(APP_ROOT, 'files')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        print(file)
        filename = file.filename
        destination = '/'.join([target, filename])
        print(destination)
        file.save(destination)
        if '.xml' in destination:
            doc = minidom.parse(destination)
            items = doc.getElementsByTagName('string')
            listName = []
            listValue = []
            for item in items:
                listName.append(item.attributes['name'].value)
                data = item.firstChild
                listValue.append(data.data if data else '')
            targetExcel = os.path.join(APP_ROOT, 'excels')
            if not os.path.isdir(targetExcel):
                os.mkdir(targetExcel)
            workbook = xlsxwriter.Workbook('/'.join([targetExcel, 'localize.xlsx']))
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'Name')
            worksheet.write('B1', 'Value')
            worksheet.write_column('A2',listName)
            worksheet.write_column('B2',listValue)
            workbook.close()

    return render_template('complete.html',path = 'localize.xlsx')


@app.route('/download-files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='excels', filename=filename,as_attachment=True)


if __name__ == '__main__':
    app.run(port=3555, debug=True)
