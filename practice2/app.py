from flask import Flask, url_for

# http://jinja.pocoo.org/docs/2.10/ ( template )

app = Flask(__name__)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'Hello Flask'


@app.route('/')
def index():
    return 'The static url is : %s' % (url_for('static', filename='js/main.js'))
