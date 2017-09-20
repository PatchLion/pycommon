from app import app, wechat
from flask import request
from flask import make_response
from flask import redirect
from flask import abort

@app.route('/')
@app.route('/index')
def index():
    return "欢迎光临狮子的小窝"

@app.route('/badrequest')
def bad_request():
    return "Bad Request", 404

@app.route('/redirect_to')
def redirect_to():
    return redirect("/badrequest")


@app.route('/abort_')
def abort_():
    return abort(203)

@app.route('/makeresponse')
def makeresponse():
    response = make_response("set cookies!")
    response.set_cookie("name", "patchlion")
    return response

@app.route('/wechat/check', methods=['GET', 'POST'])
def wechat_check():
    if request.method == 'POST':
        wechat.parse_data(request.data)
        content = wechat.message.content  # 对应于 XML 中的 Content
        return wechat.response_text("你说的是:" + content, escape=False)
    else:
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")

        if wechat.check_signature(signature, timestamp, nonce):
            return echostr
        else:
            return "failed"
