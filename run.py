from flask import Flask

# Initialising the App
app = Flask(__name__)


# Sets up routing using decorators - This is index (http://www.example.com/)
@app.route("/")
def index():
    return "<h1>Hello World</h1>"

# Temporary conditional to run if the file is the main exec
if __name__ == "__main__":
    app.run()