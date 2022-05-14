from flask import Flask, render_template, url_for
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Here we do some funky stuff, and change the session'




@app.route('/')
def home():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True) #runs a local server on port 5000