import threading
import time
from rbp_camera import *
from ultralytics import YOLO
from flask import Flask, request, render_template, redirect, jsonify

app = Flask(__name__)
model = YOLO('/home/rohan/Desktop/zenith2024/models/Final.pt')

user = {}

item_price_map = {
    "B-Natural Mango": 10,
    "Bingo Very Peri-Peri": 20,
    "Cofsils": 35,
    "Dark Fantasy Choco Fills": 40,
    "Dark Fantasy Nut Fills": 40,
    "Fiama Sandalwood Gel Bar": 40,
    "Galaxy Buds Pro": 16000,
    "Head & Shoulders": 82,
    "Kitkat": 25,
    "Tata Coffee": 55,
    "Yippee Noodles": 14,
}

current_bill = {}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        email = request.form['email']
        phone = request.form['phone']
        user['email'] = email
        user['phone'] = phone
        return redirect("/billing")

@app.route("/billing", methods=["GET", "POST"])
def billing():
    # t1 = threading.Thread(target=update_bills, args=(10,))
    # t1.start()
    return render_template("bill.html", bill=current_bill, email=user.get("email"), phone=user.get("phone"))

@app.route("/get_items", methods=["GET"])
def get_items():
    return jsonify(current_bill)

# def update_bills(time_interval):
#     global current_bill
#     start_camera()
#     while True:
#         time.sleep(time_interval)
#         img_path = capture_frame()
#         results = model.predict(img_path)
#         result = results[0]
#         names = result.names
        
#         for i in range(len(result.boxes)):
#             box = result.boxes[i]
#             print('Object: ', names[box.cls[0].item()])
#             current_bill = jsonify(names[box.cls[0].item()])
        
if __name__ == "__main__":  
    app.run(debug=True)