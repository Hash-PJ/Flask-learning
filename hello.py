from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():     #function name and url route name are independent. unique function names should be used.
    return "<p>Hello World!</p>"

if __name__=="__main__":
    app.run(debug=True)  #cmd: $ <py -m flask --app hello run> or <flask --app hello run>
