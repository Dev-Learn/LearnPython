from flask import Flask, url_for, render_template, request, make_response,session,escape
import os

# http://jinja.pocoo.org/docs/2.10/ ( template )

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'Hello Flask'


@app.route('/')
def index():
    return 'The static url is : %s' % (url_for('static', filename='js/mainWindow.js'))

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

@app.route('/testCookieSession')
def testCookieSession():
    # get cookie from request object sent from browsers
    var_1 = request.cookies.get('test')
    var_2 = 'test Cookie'

    var_3 = 'abcdef'

    if 'idsession' in session:
        print('The key is available. Got from session')
        var_3 = escape(session['idsession'])
    else:
        print('The session does have the key. Now generate new one')
        session['idsession'] = var_3

    template = render_template('test_cookie_session_template.html', var1=var_1, var2=var_2,var3 = var_3)
    resp = make_response(template)
    # set cookie from request object sent from server
    # resp.set_cookie('test', 'Nam Tran')
    return resp
