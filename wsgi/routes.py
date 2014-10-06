import os
from flask import Flask

app = Flask(_name_)
app.config['PROPOGATE_EXCEPTIONS'] = True

@app.route("/")
def insult():
    return "Hello, code monkey!"

if __name__ == "__main__":
    app.run()
