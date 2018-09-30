from flask import Flask, url_for,render_template

# http://jinja.pocoo.org/docs/2.10/ ( template )

app = Flask(__name__)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'Hello Flask'


@app.route('/')
def index():
    return 'The static url is : %s' % (url_for('static', filename='js/main.js'))

@app.route('/testtemplate')
def testTemplate():
    nav = [
            # {"href" : url_for("testTemplate") ,"caption" : "Test Render Template Page"},
            {"href" : url_for("test") ,"caption" : "Hello Page"}
           ]
    return render_template('test_template.html',val = 'Test',nav = nav)

@app.route('/testExtendTemplate')
def testExtendTemplate():
    return render_template('test_extend_template.html')
