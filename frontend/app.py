from flask import Flask, render_template, url_for, request, send_file, redirect
import csv
import os.path
from os import path

app = Flask(__name__)
text = "empty"
text_area = False

@app.route('/')
def index():
    return render_template('index.html', dl_visible="none", err_visible="none")

@app.route("/", methods=["POST"])
def submit():
    global text
    text = request.form['text']
    if path.exists('language_decks/' + text + '.csv'):
        return render_template('index.html', dl_visible="inline-block", err_visible="none") 
    return render_template('index.html', dl_visible="none", err_visible="block") 

@app.route("/getCSV")    
def getCSV():
    global text
    try:
        filename = text.lower() + ".csv"
        return send_file('language_decks/' + filename, mimetype='text/csv', attachment_filename=filename, as_attachment=True)
    except:
        return redirect(url_for('index'))


@app.route("/adv")
def convText():
    global text_area
    if text_area:
        text_area = False
        return redirect(url_for('index'))
    else:
        text_area = True
        return render_template('index.html', dl_visible="none", err_visible="none", text_area=True)  

if __name__ == "__main__":
    app.run(debug=True)