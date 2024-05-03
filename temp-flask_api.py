from flask import Flask, request, render_template, redirect, jsonify
import threading
import time
# import rbp_camera as camera
# from ultralytics import YOLO

app = Flask(__name__)
# model = YOLO('/home/rohan/Desktop/zenith2024/models/Final.pt')

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

current_bill = {
    "B-Natural Mango": [10, 3, 10],
    "Bingo Very Peri-Peri": [20, 3, 20],
    "Cofsils": [35, 3, 35],
    "Dark Fantasy Choco Fills": [40, 3, 40],
    "Dark Fantasy Nut Fills": [40, 3, 40],
    "Fiama Sandalwood Gel Bar": [40, 3, 40],
    "Galaxy Buds Pro": [16000, 3, 16000],
    "Head & Shoulders": [82, 3, 82],
    "Kitkat": [25, 3, 25],
    "Tata Coffee": [55, 3, 55],
    "Yippee Noodles": [14, 3, 14],
    }

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

@app.route("/delete_item", methods=["POST"])
def delete_item():
    item = request.form['item']
    security_code = request.form['security_code']


    if security_code != "1234":
        return jsonify("Incorrect Code!")
    
    current_data = current_bill[item]

    if current_data[1] == 1:
        del current_bill[item]
    else:
        current_bill[item] = [current_data[0], current_data[1] - 1, (current_data[0] * (current_data[1] - 1))]
    
    return get_items()



def update_bills(time_interval):
    camera.start_camera()
    global current_bill
    while True:
        time.sleep(time_interval)
        img_path = camera.capture_frame()
        print(img_path)
        results = model.predict(img_path)

        result = results[0]
        names = result.names
			
        for i in range(len(result.boxes)):
            box = result.boxes[i]
            object_name = names[box.cls[0].item()]
            print('Object: ', names[box.cls[0].item()])
        
            if object_name in current_bill:
                current_bill[object_name][1] += 1
                current_bill[object_name][2] = (current_bill[object_name][0] * current_bill[object_name][1])
            else:
                current_bill[object_name] = [item_price_map[object_name], 1, item_price_map[object_name]]
        
if __name__ == "__main__":  
    app.run(debug=True)