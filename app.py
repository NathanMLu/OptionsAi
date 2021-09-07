from flask import Flask, request, jsonify, render_template, redirect
from tda import auth, client

import os
import json
import datetime

# If it is running locally or on heroku servers
local = False
if os.path.exists('local.txt'):
    local = True

# If  user is verified or not
verified = False

# Loading in config file if it exists (depends on server or localhost)
if local == True:
    import config

# Generates new Flask app
app = Flask(__name__)

# Creates token file if it has not been created
if local == True:
    c = auth.client_from_token_file('token', config.apikey)
else:
    # Creates the token file 
    f = open("token", "w")
    embed = {"access_token": os.environ["ACCESS_TOKEN"],
            "scope": os.environ["SCOPE"],
            "expires_in": int(os.environ["EXPIRES_IN"]),
            "token_type": os.environ["TOKEN_TYPE"],
            "expires_at": int(os.environ["EXPIRES_AT"]),
            "refresh_token": os.environ["REFRESH_TOKEN"]}
    token = {"creation_timestamp": int(os.environ["CREATION_TIMESTAMP"]),
            "token": embed}
    f.write(json.dumps(token))

    # Creating client
    f = open("token", "r")
    c = auth.client_from_token_file('token', os.environ["API_KEY"])

# Default route leads to authentication
@app.route('/')
def auth():
    return render_template('homepage.html')

@app.route('/form', methods = ['GET', 'POST'])
def form():
    global local, verified
    error = None
    if request.method == 'POST':
        form_data = request.form
        if local == True:
            if form_data['username'] != config.optionsai_username or form_data['password'] != config.optionsai_password:
                error = 'Error! Access Denied! 🔫'
        else:
            if form_data['username'] != os.environ['OPTIONSAI_USERNAME'] or form_data['password'] != os.environ['OPTIONSAI_PASSWORD']:
                error = 'Error! Access Denied! 🔫'
        
        if error != None:
            return render_template('auth.html', error = error)
        else:
            verified = True
            return redirect('/controlpanel')
    else:
        return render_template('auth.html')

@app.route('/controlpanel')
def controlpanel():
    return render_template('controlpanel.html')


@app.route('/quote/<string:symbol>')
def quote(symbol):
    response = c.get_quote(symbol)
    return response.json()

@app.route('/option/chain/<string:symbol>')
def option_chain(symbol):
    response = c.get_option_chain(symbol)
    return response.json()

@app.route('/option/order', methods=['POST'])
def option_order():
    webhook_message = app.current_request.json_body

    print(webhook_message)

    if 'passphrase' not in webhook_message:
        return {
            "code": "error",
            "message": "no passphrase, c'mon at least try something..."
            
        }
    if webhook_message['passphrase'] != os.environ["SECRET_CODE"]:
        return {
            "code": "error",
            "message": "wrong passphrase buddy. good try but not good enough :)"
        }
    else:
        order_spec = {
            "complexOrderStrategyType": "NONE",
            "orderType": "LIMIT",
            "session": "NORMAL",
            "price": webhook_message["price"],
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                "instruction": "BUY_TO_OPEN",
                "quantity": webhook_message["quantity"],
                "instrument": {
                    "symbol": webhook_message["symbol"],
                    "assetType": "OPTION"
                }
                }
            ]
        }

        response = c.place_order(os.environ["ACCOUNT_ID"], order_spec)

        return{
            "code": "order placed!"
        }
        