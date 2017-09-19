from app import app, wechat
from flask import request

@app.route('/')
@app.route('/index')
def index():
    return "欢迎光临狮子的小窝"

@app.route('/wechat/check')
def wechat_check():
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")

    if wechat.check_signature(signature, timestamp, nonce):
        return echostr
    else:
        return "failed"
