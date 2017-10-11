from app import app, wechat
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask import render_template
import base64
import sys, json, os
sys.path.insert(0, "C:\\Users\\Administrator\\Documents\\GitHub\\python_commons\\")
from Projects.Spiders.Spiders.datas.PicturesSession import allImageListFromDB
all_images = allImageListFromDB()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/badrequest')
def bad_request():
    return "Bad Request", 404

@app.route('/redirect_to')
def redirect_to():
    return redirect("/badrequest")


class Myobj(object):
    def __init__(self, name):
        self.name = name

    def getname(self):
        return self.name

@app.route('/vars')
def vars():
    mydict = {'key1': '123', 'key': 'hello'}
    mylist = (123, 234, 345, 789)
    myintvar = 0
    myobj = Myobj('Hyman')
    return render_template('vars.html', mydict=mydict, mylist=mylist, myintvar=0, myobj=myobj)

def imageurls2json(urls, start, end):
    j = {}
    j["state"] = 0
    j["images"] = urls
    j["total_size"] = len(all_images)
    j["size"] = end - start + 1
    j["start"] = start
    j["end"] = end
    print(j)
    encode_json = json.dumps(j)
    return encode_json

@app.route('/all')
def all():
    global all_images
    return imageurls2json(all_images, 0, len(all_images)-1)


@app.route('/post_image', methods=["POST"])
def post_image():
    #print("post_image:", request.form, request.method)
    if request.method == "POST":
        tempdata = request.get_data()
        string = str(base64.b64decode(tempdata), encoding='utf-8')
        datasplit = string.split("|")

        if len(datasplit) == 3:
            path = datasplit[0]
            name = datasplit[1]
            data = datasplit[2]

            if not os.path.exists(path):
                os.mkdir(path)

            fullpath = path + "/" + name
            with open(fullpath, "wb",) as f:
                print("Write file to:", fullpath)
                f.write(base64.b64decode(data))
        return "{'state':0}"
    else:
        return "{'state':-1}"

@app.route('/all/size')
def all_size():
    global all_images
    return str(len(all_images))

@app.route('/all/refresh')
def all_refresh():
    global all_images
    all_images = allImageListFromDB()
    return imageurls2json(all_images, 0, len(all_images)-1)

@app.route('/all/limit/<num>')
def all_limit(num):
    global all_images
    number = int(num)
    return imageurls2json(all_images[:number], 0, number-1)

@app.route('/all/range/<start>/<size>')
def all_range(start, size):
    global all_images
    st = int(start)
    sz = int(size)
    return imageurls2json(all_images[st:(st+sz)], st, st+sz)

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
