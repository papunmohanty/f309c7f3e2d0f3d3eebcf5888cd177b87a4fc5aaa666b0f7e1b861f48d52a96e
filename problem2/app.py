from flask import Flask

from .scrapping import scrapper

app = Flask(__name__)


@app.route("/v1/covid/summary/all", methods=["GET"])
def summaries():
    response = scrapper()
    return {"summary": response}


@app.route("/v1/covid/summary/<country>", methods=["GET"])
def summary(country):
    try:
        response = scrapper(country)
    except Exception as err:  # noqa: F841
        return {"message": "Internal Server Error"}, 500
    if response == "Country not found":
        return {"message": "Country not found"}, 404
    else:
        return {"summary": response}


if __name__ == "__main__":
    app.run()
