from app import app
from flask import jsonify, request
from flask_cors import CORS
import json
import requests
import bs4
from datetime import datetime

# things that should have been imported from namefeature module
class NameNotFoundException(Exception):
    pass

def logVisits(indexNumber, name):
    file = open("logs.txt", "a")
    file.write(f"{datetime.now()} --- {indexNumber} --- {name}\n")

def getName(index_no):
    url1 = "https://online.crdbbank.co.tz/apply/search"
    url2 = "https://online.crdbbank.co.tz/apply/heslbInquiry"
    form_data = {"application_type": "HESLB", "application_ref":index_no}

    resp1 = requests.post(url1, data=form_data)
    cookies = resp1.headers['Set-Cookie']
    json_resp1 = json.loads(resp1.text)

    # filter cookies from all the headers
    my_cookies = {}
    items = []

    for item1 in cookies.split(";"):
        for item2 in item1.split("="):
            items.append(item2)

    index = 0
    for i in items:
        if "cp_session_secure" in i:
                my_cookies[i] = items[index+1]

        if "BIGipServerCRDB" in i:
            my_cookies[i.split(",")[1].strip()] = items[index+1]

        index += 1

    # figure if the index number has a loan, meaning name can be obtained
    if "uri" in json_resp1["data"]:
        name = ""
        resp2 = requests.post(url2, data=form_data, cookies=my_cookies)

        # use bs4 to scrap name
        soup = bs4.BeautifulSoup(resp2.text, features="html.parser")
        name = soup.find_all("h1")[0].text.strip()

        return name
    else:
        raise(NameNotFoundException("Failed to Fetch Name! Possibly not Available from our Sources"))

CORS(app)

@app.route("/")
def home():
    logVisits("sbjsbdjfs", "aksjnkajnd")
    return "boomboomboom.com"

@app.route("/status", methods=["POST"])
def register():
    if request.method == "POST":
        indexNumber = request.form["indexNumber"]

        if indexNumber:
            try:
                name = getName(indexNumber)
                resp = jsonify({'code': 200, 'message': {'name': name, 'hasBoom': 'yes'}})
                logVisits(indexNumber, name)
                return resp
            except NameNotFoundException as nnfe:
                print(nnfe)
                resp = jsonify({'code': 200, 'message': {'name': indexNumber, 'hasBoom': 'no'}})
                logVisits(indexNumber, "Name Not Found")
                return resp
            except Exception as e:
                print(e)
                resp = jsonify({'code': 500, 'message': 'an internal server error occured'})
                return resp
        else:
            resp = jsonify({'code': 400, 'message': 'index number not provided'})
            return resp
    else:
        resp = jsonify({'code': 405, 'message': 'method not allowed'})
        return resp