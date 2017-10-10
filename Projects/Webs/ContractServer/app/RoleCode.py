'''
超级管理员 	0 	所有操作
基础管理 	1 	包含角色管理和公司管理
用户管理 	2 	用户的新增、删除、修改、权限修改、角色修改
项目管理 	3 	项目的新增、删除（审批完成前）、修改（审批完成前）、审批
项目查询 	4 	项目数据查看
合同管理 	5 	合同的新增、删除、修改、附件管理
合同查询 	6 	合同数据查看
报表管理 	7 	报表查询、导出
公司相关 	8 	存在，查询的数据全部进行公司过滤
'''
Auth_Root = 0
Auth_Base = 1
Auth_User = 2
Auth_Project = 3
Auth_ProjectQuery = 4
Auth_Contract = 5
Auth_ContractQuery = 6
Auth_Report = 7
Auth_Company = 8


AuthNames = {
    Auth_Root:"超级管理员",
    Auth_Base: "基础管理",
    Auth_User:"用户管理",
    Auth_Project:"项目管理",
    Auth_ProjectQuery:"项目查询",
    Auth_Contract:"合同管理",
    Auth_ContractQuery:"合同查询",
    Auth_Report:"报表管理",
    Auth_Company:"公司管理"
}