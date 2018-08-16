from flask import Flask, flash, render_template, request, redirect, url_for
import json
import requests

app = Flask(__name__)
app.secret_key = "First Code Academy"


class content():
    translation = ""
    choice = ""
    text = ""


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if not request.form['text']:
            flash('Please input text for translation.', 'Error')
        else:
            content.text = request.form['text']
            content.choice = request.form['choice']
            uri = "https://api.funtranslations.com/translate/" + content.choice + ".json"
            payload = {'text': content.text}

            try:
                r = requests.get(uri, params=payload)
            except requests.ConnectionError:
                flash('Connection Error', 'error')
                return redirect(url_for('home'))

            jr = r.text
            data = json.loads(jr)

            if data["error"]["message"]:
                flash(data["error"]["message"], 'error')
            else:
                content.translation = data["contents"]["translated"]
                flash(content.choice + '\'s translation is: ' + content.translation, 'success')

        return redirect(url_for('home'))

    return render_template("main.html")


if __name__ == '__main__':
    app.run()
