import functools, json
from json import JSONDecodeError
from .responsebuilder import ApiResponseBuilder

def flaskResponse(func):
    @functools.wraps(func)
    def wrapper(request,args):
        supports_methods = ["POST", "GET"]
        #print(request.method)
        if request.method in supports_methods:
            args = {}
            if "POST" == request.method:
                json_data = request.get_data()
                if json_data is not None and len(json_data) > 0:
                    try:
                        if isinstance(json_data, bytes):
                            args = json.loads(str(json_data, encoding='utf-8'))
                        else:
                            args = json.loads(json_data)
                    except JSONDecodeError as e:
                        return ApiResponseBuilder.build(code=-1, msgExt="无效的数据格式(JSON)")
            elif "GET" == request.method:
                args = request.args
                #print("GET args:", args)
            return func(None, args)
        else:
            return ApiResponseBuilder.build(code=-1, msgExt="不支持的请求方法: " + request.mothod)
    return wrapper