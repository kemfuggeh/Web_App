from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hardcoded username and password
correct_username = "user"
correct_password = "pass666"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == correct_username and password == correct_password:
        return redirect(url_for('index'))
    else:
        return render_template('login.html', message='Incorrect username or password')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
