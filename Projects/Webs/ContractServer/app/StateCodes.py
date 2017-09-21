
StateCode_Success = 0
StateCode_UserExist = 1001
StateCode_UnsupportMethod = 1002
StateCode_InvaildParam = 1003
StateCode_FailedCreateUser = 1004
StateCode_InvaildDataFormat = 1005
StateCode_FailedToLogin = 1006

StateCodeDescriptions = {StateCode_Success : "成功",
                         StateCode_UserExist : "用户已存在",
                         StateCode_UnsupportMethod : "不支持的方法",
                         StateCode_InvaildParam : "无效的参数",
                         StateCode_FailedCreateUser: "创建用户失败",
                         StateCode_InvaildDataFormat: "无效的数据格式",
                         StateCode_FailedToLogin: "登录失败"}


#获取代码描述
def codeString(code):
    if code in StateCodeDescriptions.keys():
        return StateCodeDescriptions[code]
    else:
        return "未知代码"