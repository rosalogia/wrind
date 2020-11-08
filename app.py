from flask import Flask, render_template, url_for, request, send_file, redirect
import csv
import os.path
import os
from os import path
from urllib.parse import quote as urlquote, unquote as urlunquote
from media_input.media_grabber import router

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", dl_visible="none", err_visible="none")


@app.route("/", methods=["POST"])
def submit():
    text = request.form["text"]
    if path.exists("language_decks/" + text + ".csv") or "wikipedia" in text:
        return render_template(
            "index.html",
            dl_visible="inline-block",
            err_visible="none",
            textfile=urlquote(text, safe=""),
        )
    return render_template("index.html", dl_visible="none", err_visible="block")


@app.route("/getCSV/<path:textfile>")
def getCSV(textfile):
    text = urlunquote(textfile)
    print(text)
    try:
        filename = text.lower() + ".csv"
        return send_file(
            "language_decks/" + filename,
            mimetype="text/csv",
            attachment_filename=filename,
            as_attachment=True,
        )
    except:
        router(text)
        return send_file(
            "set_1.csv",
            mimetype="text/csv",
            attachment_filename="set_1.csv",
            as_attachment=True,
        )


@app.route("/adv")
def convText():
    return render_template(
        "index.html", dl_visible="none", err_visible="none", text_area=True
    )


app.config["FILE_UPLOADS"] = "./uploads"


@app.route("/adv", methods=["GET", "POST"])
def advancedSubmit():
    print("Subtitle Saved")
    if request.method == "POST":
        try:
            text = request.form["text"]
            print(text)
            router(text, url=False)
            return send_file(
                "set_1.csv",
                mimetype="text/csv",
                attachment_filename="set_1.csv",
                as_attachment=True,
            )
        except ValueError:
            subtitle = request.files["file"]
            print(subtitle)
            subtitle.save(os.path.join(app.config["FILE_UPLOADS"], subtitle.filename))
            router("uploads/" + subtitle.filename, url=False)
            os.remove("./uploads/" + subtitle.filename)
            return send_file(
                "set_1.csv",
                mimetype="text/csv",
                attachment_filename="set_1.csv",
                as_attachment=True,
            )

    return redirect(url_for("index"))


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


if __name__ == "__main__":
    app.run(debug=True)
