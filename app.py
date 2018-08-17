from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sslify import SSLify
import json
import requests

app = Flask(__name__)
app.secret_key = "First Code Academy"
# sslify = SSLify(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    text = ""

    if request.method == 'POST':
        if not request.form['text']:
            flash('Please input text for translation.', 'Error')
        else:
            text = request.form['text']
            choice = request.form['choice']
            uri = "https://api.funtranslations.com/translate/" + choice + ".json"
            payload = {'text': text}

            try:
                r = requests.get(uri, params=payload)
            except requests.ConnectionError:
                flash('Connection Error', 'error')
                return redirect(url_for('home'))

            jr = r.text
            data = json.loads(jr)

            try:
                translation = data["contents"]["translated"]
                flash(choice + '\'s translation is: ' + translation, 'success')
            except (KeyError):
                flash(data["error"]["message"], 'error')

        return redirect(url_for('home'))

    return render_template("main.html", text=text)


if __name__ == '__main__':
    app.run()
