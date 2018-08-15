from flask import Flask, flash, render_template, request
import json
import requests

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':

        text = request.form['text']
        choice = request.form['choice']
        uri = "https://api.funtranslations.com/translate/" + choice + ".json"
        payload = {'text': text}

        try:
            uResponse = requests.get(uri, params=payload)
        except requests.ConnectionError:
            flash("Connection Error", 'error')
            return "Connection Error"

        Jresponse = uResponse.text
        data = json.loads(Jresponse)

        translation = data['contents']['translated']

    return render_template("main.html", translation=translation)


if __name__ == '__main__':
    app.run(debug = True)
