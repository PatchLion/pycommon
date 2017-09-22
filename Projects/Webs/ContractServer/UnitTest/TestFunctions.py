import requests
import json

SERVER = "http://182.61.25.137:5000"

def get(api, param, equlfunc, compares):
    url = SERVER + api
    print("GET", url, "With", param)
    res = requests.get(url=url, params=param)
    return resolve_response(res, equlfunc, compares)

def post(api, param, equlfunc, compares):
    url = SERVER + api
    data = json.dumps(param, ensure_ascii=False)
    print("POST", url, "With", type(data), data)
    res = requests.post(url=url, data=data)
    return resolve_response(res, equlfunc, compares)


def resolve_response(res, equlfunc, compares):
    ret = None
    if 200 != res.status_code:
        ret = res.status_code, -1, res.reason, {}
    else:
        content = res.content.decode(encoding='utf-8')
        #print(res.status_code, content)
        data = json.loads(content)
        #print(data["state"], data["message"], data["data"])
        ret = res.status_code, data["state"], data["message"], data.get("data", {})

    print("Result:", "|", str(ret[0]), "|", str(ret[1]), "|", '"'+ret[2]+'"',"|", str(ret[3]))

    if len(compares) >= 1:
        equlfunc(ret[0], compares[0])
    if len(compares) >= 2:
        equlfunc(ret[1], compares[1])
    #return ret


