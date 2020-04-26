from flask import Flask, render_template, request, redirect, send_file
from job_korea import get_jobs
import save

app = Flask("WebCrawling")

db = {}


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/search")
def search():
    word = request.args.get("word")
    if word:
        word = word.lower()
        check_db = db.get(word)
        if check_db:
            jobs = check_db
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("result.html",  searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route("/save")
def save_file():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save.save_to_csv(jobs)
        return send_file("jobs.csv", mimetype="text/csv", attachment_filename=f"{word}.csv", as_attachment=True)
    except:
        return redirect("/")


app.run(host="0.0.0.0", port=8000)
