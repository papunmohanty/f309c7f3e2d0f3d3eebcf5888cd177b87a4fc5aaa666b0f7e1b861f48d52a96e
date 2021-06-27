from flask import Flask, render_template

from .scrapping import scrapper

app = Flask(__name__)


@app.route("/api/v1/covid/summary/all", methods=["GET"])
def summaries():
    response = scrapper()
    return {"summary": response}


@app.route("/api/v1/covid/summary/<country>", methods=["GET"])
def summary(country):
    try:
        response = scrapper(country)
    except Exception as err:  # noqa: F841
        return {"message": "Internal Server Error"}, 500
    if response == "Country not found":
        return {"message": "Country not found"}, 404
    else:
        return {"summary": response}


@app.route("/covid/summary", methods=["GET"])
def summaries_page():
    response = scrapper()
    return render_template("covidcases.html", countries=response)


if __name__ == "__main__":
    app.run()
