from flask import Flask, render_template, url_for, request, send_file, redirect
import csv
import os.path
from os import path
from media_input.media_grabber import router

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
    if path.exists('language_decks/' + text + '.csv') or 'wikipedia' in text:
        return render_template('index.html', dl_visible="inline-block", err_visible="none") 
    return render_template('index.html', dl_visible="none", err_visible="block") 

@app.route("/getCSV")    
def getCSV():
    global text
    print(text)
    try:
        filename = text.lower() + ".csv"
        return send_file('language_decks/' + filename, mimetype='text/csv', attachment_filename=filename, as_attachment=True)
    except:
        router(text)
        return send_file('set_1.csv', mimetype='text/csv', attachment_filename='set_1.csv', as_attachment=True)


@app.route("/adv")
def convText():
    global text_area
    if text_area:
        text_area = False
        return redirect(url_for('index'))
    else:
        text_area = True
        return render_template('index.html', dl_visible="none", err_visible="none", text_area=True)  

@app.route('/getFile', methods=['GET', 'POST'])
def advancedSubmit():
    if request.method == "POST":
        if request.files:
            subtitles = request.files["srt"]
            print(subtitles)
            return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)