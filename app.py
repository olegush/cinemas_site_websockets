import os
from dotenv import load_dotenv
from flask import Flask, render_template


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    load_dotenv()
    host = os.environ.get('HOST')
    port = int(os.environ.get('PORT', 5500))
    app.run(host=host, port=port)
