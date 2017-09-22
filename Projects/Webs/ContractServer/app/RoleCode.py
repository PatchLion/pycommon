'''
管理员 	0 	所有操作
项目管理 	1 	项目的新增、删除（审批完成前）、修改（审批完成前）、审批
角色管理 	2 	角色的新增、删除、修改、权限修改
用户管理 	3 	用户的新增、删除、修改、权限修改、角色修改
公司管理 	4 	公司的新增、删除、修改
报表管理 	5 	报表查询、导出
合同管理 	6 	合同的新增、删除、修改、附件管理
'''
Auth_Root = 0
Auth_Project = 1
Auth_Role = 2
Auth_User = 3
Auth_Company = 4
Auth_Report = 5
Auth_Contract = 6

AuthNames = {
    Auth_Root:"根管理",
    Auth_Project:"项目管理",
    Auth_Role:"角色管理",
    Auth_User:"用户管理",
    Auth_Company:"公司管理",
    Auth_Report:"报表管理",
    Auth_Contract:"合同管理"
}