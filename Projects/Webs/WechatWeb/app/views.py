from app import app, wechat
from flask import request

@app.route('/')
@app.route('/index')
def index():
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")

    return wechat.check_signature(signature, timestamp, nonce)
