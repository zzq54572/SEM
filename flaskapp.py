from flask import Flask
flask_app=Flask(__name__)
flask_app.config['SECRET_KEY']='flasksecret'

if __name__=="__main__":
    flask_app.run(debug=True)