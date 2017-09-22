
StateCode_Success = 0
StateCode_UserExist = 1001
StateCode_UnsupportMethod = 1002
StateCode_InvaildParam = 1003
StateCode_FailedCreateUser = 1004
StateCode_InvaildDataFormat = 1005
StateCode_FailedToLogin = 1006
StateCode_UserNotExist = 1007
StateCode_ProjectExist = 1008
StateCode_FailedToCreateProject = 1009
StateCode_ContractExist = 1010
StateCode_FailedToCreateContractHistory = 1011
StateCode_FailedToCreateCompany = 1012
StateCode_CompanyExist = 1013
StateCode_ContractNotExist = 1014
StateCode_ProjectNotExist = 1015
StateCode_FileExist = 1015
StateCode_RoleExist = 1016
StateCode_FailedToCreateRole = 1017

StateCodeDescriptions = {
StateCode_Success : "成功",
StateCode_UserExist : "用户已存在",
StateCode_UnsupportMethod : "不支持的方法",
StateCode_InvaildParam : "无效的参数",
StateCode_FailedCreateUser: "创建用户失败",
StateCode_InvaildDataFormat: "无效的数据格式",
StateCode_FailedToLogin: "登录失败",
StateCode_UserNotExist: "用户不存在",
StateCode_ProjectExist: "项目已存在",
StateCode_FailedToCreateProject: "创建项目失败",
StateCode_ContractExist: "合同已存在",
StateCode_FailedToCreateContractHistory: "创建合同历史记录失败",
StateCode_FailedToCreateCompany: "创建公司失败",
StateCode_CompanyExist: "公司已存在",
StateCode_ContractNotExist: "合同不存在",
StateCode_ProjectNotExist: "项目不存在",
StateCode_FileExist: "文件已存在",
StateCode_RoleExist: "角色已存在",
StateCode_FailedToCreateRole: "创建角色失败"
}


#获取代码描述
def codeString(code):
    if code in StateCodeDescriptions.keys():
        return StateCodeDescriptions[code]
    else:
        return "未知代码"