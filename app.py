from flask import Flask, flash, render_template, request, redirect, url_for
import json
import requests

app = Flask(__name__)

translation = ""

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if not request.form['text']:
            flash('Please input text for translation.', 'Error')
        else:
            text = request.form['text']
            choice = request.form['choice']
            uri = "https://api.funtranslations.com/translate/" + choice + ".json"
            payload = {'text': text}

            try:
                uResponse = requests.get(uri, params=payload)
            except requests.ConnectionError:
                flash('Connection Error', 'Error')
                return redirect(url_for('home'))

            jresponse = uResponse.text
            data = json.loads(jresponse)

            translation = data['contents']['translated']
            flash(choice + '\'s translation is: \n' + translation, 'Success')

    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug = True)
