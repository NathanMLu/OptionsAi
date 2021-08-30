from flask import Flask, request, jsonify
from tda import auth, client
import os

app = Flask(__name__)

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    f = open("test.txt", "w")
    f.write(os.environ['ACCOUNT_ID'])
    f = open("test.txt", "r")
    ret = f.read()

    return ret


"""
from flask import Flask
from tda import auth, client

import os
import json
import datetime
import config

application = Flask(__name__)

c = auth.client_from_token_file(config.token_path, config.api_key)

@application.route('/')
def index():
    return "Hello World"

@application.route('/quote/<string:symbol>')
def quote(symbol):
    response = c.get_quote(symbol)
    return response.json()

@application.route('/option/chain/<string:symbol>')
def option_chain(symbol):
    response = c.get_option_chain(symbol)
    return response.json()

@application.route('/option/order', methods=['POST'])
def option_order():
    webhook_message = application.current_request.json_body

    print(webhook_message)

    if 'passphrase' not in webhook_message:
        return {
            "code": "error",
            "message": "no passphrase, c'mon at least try something..."
            
        }
    if webhook_message['passphrase'] != config.secretcode:
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

        response = c.place_order(config.account_id, order_spec)

        return{
            "code": "order placed!"
        }
"""