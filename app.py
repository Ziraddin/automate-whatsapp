import flask
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

app = Flask(_name_)

# Connect to MongoDB
cluster = MongoClient("mongodb+srv://Saddam:Matrixgame213@wpbotdatabase."
                      "giznbjw.mongodb.net/?retryWrites=true&w=majority",
                      tls=True, tlsAllowInvalidCertificates=True)
db = cluster["botDB"]
users = db["users"]
orders = db["orders"]def handle_main_menu(number, option):
if option == 1:
return "0️⃣ Geri qayıtmaq\n"
"1️⃣ Excel\n"
"2️⃣ MOSE\n"
"3️⃣ Power BI (PL-300)\n"
"4️⃣ SQL (1Z0-071)\n"
"5️⃣ Data Analitika", "kurslar"
elif option == 2:
return "Əlaqə nömrəsi: 050-369-60-88\n"
"Email: seddamhasanov213@yandex.com", "main"
elif option == 3:
return "3 seçildi", "main"
elif option == 4:
return "4 seçildi", "main"
else:
return "Məlumat ala bilmək üçün zəhmət olmasa 1, 2, 3, 4\nrəqəmlərindən birini daxil edin", "main"

def handle_kurslar_menu(number, option):
if option == 0:
return "1️⃣ Kurslar haqqında məlumat\n"
"2️⃣ Bizimlə əlaqə\n"
"3️⃣ FAQ\n"
"4️⃣ Təlimlərimizin sillabusları\n", "main"
elif 1 <= option <= 5:
kurslar = ["Excel", "MOSE", "PowerBI (PL-300)", "SQL (1Z0-071)", "Data Analitika"]
return f"{kurslar[option - 1]} haqqında məlumat", "main"
else:
return "Məlumat ala bilmək üçün zəhmət olmasa 0, 1, 2, 3, 4, 5\nrəqəmlərindən birini daxil edin", "main"

def update_user_status(number, status):
users.update_one({"number": number}, {"$set": {"status": status}})

@app.route("/", methods=['POST'])
def sms():
number = request.form['From']
message_body = request.form['Body']user = users.find_one({"number": number})
if user is None:
    users.insert_one({"number": number, "status": "main"})
    update_user_status(number, "main")
    resp = MessagingResponse()
    resp.message("Salam, nə istəyirsiniz?")
    return str(resp)

status = user["status"]

if status == "main":
    try:
        option = int(message_body)
        response_text, new_status ="POST"])
def sms_reply():
number = request.form['From']
message_body = request.form['Body']
user = users.find_one({"number": number})if user is None:
    users.insert_one({"number": number, "status": "main"})
    user = users.find_one({"number": number})

if user["status"] == "main":
    try:
        option = int(message_body)
        response_text, next_status = handle_main_menu(number, option)
    except ValueError:
        response_text = "Məlumat ala bilmək üçün zəhmət olmasa 1, 2, 3, 4\nrəqəmlərindən birini daxil edin"
        next_status = "main"
elif user["status"] == "kurslar":
    try:
        option = int(message_body)
        response_text, next_status = handle_kurslar_menu(number, option)
    except ValueError:
        response_text = "Məlumat ala bilmək üçün zəhmət olmasa 0, 1, 2, 3, 4, 5\nrəqəmlərindən birini daxil edin"
        next_status = "kurslar"
else:
    response_text = "Səhv baş verdi, lütfən yenidən cəhd edin"
    next_status = "main"

update_user_status(number, next_status)

resp = MessagingResponse()
resp.message(response_text)
return str(resp) if name == "main":
app.run()
