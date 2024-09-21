from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    print("hi")
    return render_template('mainpage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you can handle login logic (e.g., check credentials)
        username = request.form.get('username')
        password = request.form.get('password')
        # For now, just redirecting to the main page after a login attempt
        return redirect(url_for('home'))
    return render_template('loginpage.html')

if __name__ == '__main__':
    app.run(debug=True)
