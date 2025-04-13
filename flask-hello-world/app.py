from flask import Flask

app = Flask(__name__)

@app.route('/get')
def hello_world():
    return 'Hello world\n'

@app.route('/post', methods=["POST"])
def post():
    return 'this is from post\n'

if __name__ == "__main__":
    app.run()
