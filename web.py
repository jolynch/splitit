from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/step/1', methods=['GET'])
def step1():
    return render_template('step1.html')

@app.route('/step/1', methods=['POST'])
def step1_process():
    return "the people are: " + str(request.form.getlist('people[]'))

if __name__ == '__main__':
    app.debug = True
    app.run()
