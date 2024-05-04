from flask import Flask, request, render_template, redirect, jsonify
import threading
import time
import rbp_camera as camera
from ultralytics import YOLO
from send_email import send_email
import datetime
import random

app = Flask(__name__)
model = YOLO('/home/rohan/Desktop/zenith2024/models/Final.pt')

user = {}

t1 = None

item_price_map = {
    "B-Natural Mango": 10,
    "Bingo Very Peri-Peri": 20,
    "Cofsils": 35,
    "Dark Fantasy Choco Fills": 40,
    "Dark Fantasy Nut Fills": 40,
    "Fiama Sandalwood Gel Bar": 40,
    "Galaxy Buds Pro": 16000,
    "Head & Shoulders": 82,
    "Head - Shoulders": 82,
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
    global t1
    t1 = threading.Thread(target=update_bills, args=(10,))
    t1.start()
    return render_template("bill.html", bill=current_bill, email=user.get("email"), phone=user.get("phone"))

@app.route("/get_items", methods=["GET"])
def get_items():
    return jsonify(current_bill)

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

@app.route("/end_billing", methods=["POST"])
def end_billing():
    t1.join()

    email = user['email']
    phone = user['phone']
    invoice_id = random.randint(123456, 999999)
    date = datetime.date.today().strftime('%d-%m-%Y')
    due_date = (datetime.date.today() + datetime.timedelta(1)).strftime('%d-%m-%Y')

    total = 0

    for current_bill_values in current_bill.values():
        total += current_bill_values[2]

    email_html = f'''

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title></title>
    <style type="text/css" rel="stylesheet" media="all">
        /* Base ------------------------------ */
        
        @import url("https://fonts.googleapis.com/css?family=Nunito+Sans:400,700&display=swap");
        body {{
          width: 100% !important;
          height: 100%;
          margin: 0;
          -webkit-text-size-adjust: none;
        }}
        
        a {{
          color: #3869D4;
        }}
        
        a img {{
          border: none;
        }}
        
        td {{
          word-break: break-word;
        }}
        
        .preheader {{
          display: none !important;
          visibility: hidden;
          mso-hide: all;
          font-size: 1px;
          line-height: 1px;
          max-height: 0;
          max-width: 0;
          opacity: 0;
          overflow: hidden;
        }}
        /* Type ------------------------------ */
        
        body,
        td,
        th {{
          font-family: "Nunito Sans", Helvetica, Arial, sans-serif;
        }}
        
        h1 {{
          margin-top: 0;
          color: #333333;
          font-size: 22px;
          font-weight: bold;
          text-align: left;
        }}
        
        h2 {{
          margin-top: 0;
          color: #333333;
          font-size: 16px;
          font-weight: bold;
          text-align: left;
        }}
        
        h3 {{
          margin-top: 0;
          color: #333333;
          font-size: 14px;
          font-weight: bold;
          text-align: left;
        }}
        
        td,
        th {{
          font-size: 16px;
        }}
        
        p,
        ul,
        ol,
        blockquote {{
          margin: .4em 0 1.1875em;
          font-size: 16px;
          line-height: 1.625;
        }}
        
        p.sub {{
          font-size: 13px;
        }}
        /* Utilities ------------------------------ */
        
        .align-right {{
          text-align: right;
        }}
        
        .align-left {{
          text-align: left;
        }}
        
        .align-center {{
          text-align: center;
        }}
        /* Buttons ------------------------------ */
        
        .button {{
          background-color: #3869D4;
          border-top: 10px solid #3869D4;
          border-right: 18px solid #3869D4;
          border-bottom: 10px solid #3869D4;
          border-left: 18px solid #3869D4;
          display: inline-block;
          color: #FFF;
          text-decoration: none;
          border-radius: 3px;
          box-shadow: 0 2px 3px rgba(0, 0, 0, 0.16);
          -webkit-text-size-adjust: none;
          box-sizing: border-box;
        }}
        
        .button--green {{
          background-color: #22BC66;
          border-top: 10px solid #22BC66;
          border-right: 18px solid #22BC66;
          border-bottom: 10px solid #22BC66;
          border-left: 18px solid #22BC66;
        }}
        
        .button--red {{
          background-color: #FF6136;
          border-top: 10px solid #FF6136;
          border-right: 18px solid #FF6136;
          border-bottom: 10px solid #FF6136;
          border-left: 18px solid #FF6136;
        }}
        
        @media only screen and (max-width: 500px) {{
          .button {{
            width: 100% !important;
            text-align: center !important;
          }}
        }}
        /* Attribute list ------------------------------ */
        
        .attributes {{
          margin: 0 0 21px;
        }}
        
        .attributes_content {{
          background-color: #F4F4F7;
          padding: 16px;
        }}
        
        .attributes_item {{
          padding: 0;
        }}
        /* Related Items ------------------------------ */
        
        .related {{
          width: 100%;
          margin: 0;
          padding: 25px 0 0 0;
          -premailer-width: 100%;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
        }}
        
        .related_item {{
          padding: 10px 0;
          color: #CBCCCF;
          font-size: 15px;
          line-height: 18px;
        }}
        
        .related_item-title {{
          display: block;
          margin: .5em 0 0;
        }}
        
        .related_item-thumb {{
          display: block;
          padding-bottom: 10px;
        }}
        
        .related_heading {{
          border-top: 1px solid #CBCCCF;
          text-align: center;
          padding: 25px 0 10px;
        }}
        /* Discount Code ------------------------------ */
        
        .discount {{
          width: 100%;
          margin: 0;
          padding: 24px;
          -premailer-width: 100%;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
          background-color: #F4F4F7;
          border: 2px dashed #CBCCCF;
        }}
        
        .discount_heading {{
          text-align: center;
        }}
        
        .discount_body {{
          text-align: center;
          font-size: 15px;
        }}
        /* Social Icons ------------------------------ */
        
        .social {{
          width: auto;
        }}
        
        .social td {{
          padding: 0;
          width: auto;
        }}
        
        .social_icon {{
          height: 20px;
          margin: 0 8px 10px 8px;
          padding: 0;
        }}
        /* Data table ------------------------------ */
        
        .purchase {{
          width: 100%;
          margin: 0;
          padding: 35px 0;
          -premailer-width: 100%;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
        }}
        
        .purchase_content {{
          width: 100%;
          margin: 0;
          padding: 25px 0 0 0;
          -premailer-width: 100%;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
        }}
        
        .purchase_item {{
          padding: 10px 0;
          color: #fcfdff;
          font-size: 15px;
          line-height: 18px;
        }}
        
        .purchase_heading {{
          padding-bottom: 8px;
          border-bottom: 1px solid #EAEAEC;
        }}
        
        .purchase_heading p {{
          margin: 0;
          color: #85878E;
          font-size: 12px;
        }}
        
        .purchase_footer {{
          padding-top: 15px;
          border-top: 1px solid #EAEAEC;
        }}
        
        .purchase_total {{
          margin: 0;
          text-align: right;
          font-weight: bold;
          color: #333333;
        }}
        
        .purchase_total--label {{
          padding: 0 15px 0 0;
        }}
        
        body {{
          background-color: #F2F4F6;
          color: #51545E;
        }}
        
        p {{
          color: #51545E;
        }}
        
        .email-wrapper {{
          width: 100%;
          margin: 0;
          padding: 0;
          -premailer-width: 100%;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
          background-color: #F2F4F6;
        }}
        
        .email-content {{
          width: 100%;
          margin: 0;
          padding: 0;
          -premailer-width: 100%;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
        }}
        /* Masthead ----------------------- */
        
        .email-masthead {{
          padding: 25px 0;
          text-align: center;
        }}
        
        .email-masthead_logo {{
          width: 94px;
        }}
        
        .email-masthead_name {{
          font-size: 16px;
          font-weight: bold;
          color: #A8AAAF;
          text-decoration: none;
          text-shadow: 0 1px 0 white;
        }}
        /* Body ------------------------------ */
        
        .email-body {{
          width: 100%;
          margin: 0;
          padding: 0;
          -premailer-width: 100%;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
        }}
        
        .email-body_inner {{
          width: 570px;
          margin: 0 auto;
          padding: 0;
          -premailer-width: 570px;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
          background-color: #FFFFFF;
        }}
        
        .email-footer {{
          width: 570px;
          margin: 0 auto;
          padding: 0;
          -premailer-width: 570px;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
          text-align: center;
        }}
        
        .email-footer p {{
          color: #A8AAAF;
        }}
        
        .body-action {{
          width: 100%;
          margin: 30px auto;
          padding: 0;
          -premailer-width: 100%;
          -premailer-cellpadding: 0;
          -premailer-cellspacing: 0;
          text-align: center;
        }}
        
        .body-sub {{
          margin-top: 25px;
          padding-top: 25px;
          border-top: 1px solid #EAEAEC;
        }}
        
        .content-cell {{
          padding: 45px;
        }}
        /*Media Queries ------------------------------ */
        
        @media only screen and (max-width: 600px) {{
          .email-body_inner,
          .email-footer {{
            width: 100% !important;
          }}
        }}
        
        @media (prefers-color-scheme: dark) {{
          body,
          .email-body,
          .email-body_inner,
          .email-content,
          .email-wrapper,
          .email-masthead,
          .email-footer {{
            background-color: #333333 !important;
            color: #FFF !important;
          }}
          p,
          ul,
          ol,
          blockquote,
          h1,
          h2,
          h3 {{
            color: #FFF !important;
          }}
          .attributes_content,
          .discount {{
            background-color: #222 !important;
          }}
          .email-masthead_name {{
            text-shadow: none !important;
          }}
        }}
        </style>
  </head>
  <body>
    <span class="preheader">This is an invoice for your purchase on { date }. Please submit payment by { due_date }</span>
    <table class="email-wrapper" width="100%" cellpadding="0" cellspacing="0" role="presentation">
      <tr>
        <td align="center">
          <table class="email-content" width="100%" cellpadding="0" cellspacing="0" role="presentation">
            <tr>
              <td class="email-masthead">
                ABC SuperMarket Groups
              </a>
              </td>
            </tr>
            <!-- Email Body -->
            <tr>
              <td class="email-body" width="570" cellpadding="0" cellspacing="0">
                <table class="email-body_inner" align="center" width="570" cellpadding="0" cellspacing="0" role="presentation">
                  <!-- Body content -->
                  <tr>
                    <td class="content-cell">
                      <div class="f-fallback">
                        <h1>Dear Customer,</h1>
                        <p>Thanks for shopping at ABC SuperMarket Groups. This is an invoice for your recent purchase.</p>
                        <p><strong>Email:</strong> {email} </p>
                        <p><strong>Phone:</strong> {phone} </p>
                        <table class="attributes" width="100%" cellpadding="0" cellspacing="0" role="presentation">
                          <tr>
                            <td class="attributes_content">
                              <table width="100%" cellpadding="0" cellspacing="0" role="presentation">
                                <tr>
                                  <td class="attributes_item">
                                    <span class="f-fallback">
              <strong>Amount Due:</strong> ₹{total}
            </span>
                                  </td>
                                </tr>
                                <tr>
                                  <td class="attributes_item">
                                    <span class="f-fallback">
              <strong>Due By:</strong> {due_date}
            </span>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <!-- Action -->
                        <table class="body-action" align="center" width="100%" cellpadding="0" cellspacing="0" role="presentation">
                          <tr>
                            <td align="center">
                              <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
                                <tr>
                                  <td align="center">
                                    <a href="#" class="f-fallback button button--green" target="_blank">Pay Invoice</a>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <table class="purchase" width="100%" cellpadding="0" cellspacing="0">
                          <tr>
                            <td>
                              <h3>Invoice ID: {invoice_id}</h3>
                            </td>
                            <td>
                              <h3 class="align-right">{date}</h3>
                            </td>
                          </tr>
                          <tr>
                            <td colspan="2">
                              <table class="purchase_content" width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                  <th class="purchase_heading" align="left">
                                    <p class="f-fallback">Description</p>
                                  </th>
                                  <th class="purchase_heading" align="right">
                                    <p class="f-fallback">Amount</p>
                                  </th>
                                </tr>
                                '''
    for item, details in current_bill.items():
        email_html += f'''
        <tr>
        <td  class="purchase_item"><span class="f-fallback">{item}</span></td>
        <td align="right" class="purchase_item"><span class="f-fallback">{details[1]} x ₹{details[0]}: <b>₹{details[2]}</b></span></td>
        </tr>
        '''
    email_html += f'''                    
                                <tr>
                                  <td width="80%" class="purchase_footer" valign="middle">
                                    <p class="f-fallback purchase_total purchase_total--label">Total</p>
                                  </td>
                                  <td width="20%" class="purchase_footer" valign="middle">
                                    <p class="f-fallback purchase_total">₹{total}</p>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <p>If you have any questions about this invoice, simply reply to this email or reach out to any of our branches for help.</p>
                        <p>Cheers,
                          <br>ABC SuperMarket Groups</p>
                      </div>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
'''
    
    send_email(email, email_html, True)

    return render_template("thanks.html")

if __name__ == "__main__":  
    app.run(debug=True)