from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app.Functions import stringMD5, createUuid
from MySqlAlchemy.DBOperator import *


ContractDB.initTables()

#增加角色表
admin_role_id = createUuid()
test_role1_id = createUuid()
test_role2_id = createUuid()
addOrRecord(ContractDB.session(), Roles(role_id = admin_role_id, role_name = "管理员")) #管理员权限
addOrRecord(ContractDB.session(), Roles(role_id = test_role1_id, role_name = "测试角色1")) #
addOrRecord(ContractDB.session(), Roles(role_id = test_role2_id, role_name = "测试角色2")) #

#增加角色权限
addOrRecord(ContractDB.session(), RoleAuth(role_id = admin_role_id, role_value = 0)) #
addOrRecord(ContractDB.session(), RoleAuth(role_id = test_role1_id, role_value = 0x010D)) #
addOrRecord(ContractDB.session(), RoleAuth(role_id = test_role1_id, role_value = 0x0201)) #
addOrRecord(ContractDB.session(), RoleAuth(role_id = test_role2_id, role_value = 0x0302)) #

#增加用户
addOrRecord(ContractDB.session(), User(user_id="root", password=stringMD5("root"), name="root"))
addOrRecord(ContractDB.session(), User(user_id="admin", password=stringMD5("admin"), name="Adminstrator"))
addOrRecord(ContractDB.session(), User(user_id="simple", password=stringMD5("simple"), name="SimpleLove"))
addOrRecord(ContractDB.session(), User(user_id="patchlion", password=stringMD5("patchlion"), name="打补丁的狮子"))

#关联用户角色
addOrRecord(ContractDB.session(), UserRole(user_id="root", role_id=admin_role_id))
addOrRecord(ContractDB.session(), UserRole(user_id="admin", role_id=admin_role_id))
addOrRecord(ContractDB.session(), UserRole(user_id="simple", role_id=admin_role_id))
addOrRecord(ContractDB.session(), UserRole(user_id="patchlion", role_id=admin_role_id))


#增加项目
addOrRecord(ContractDB.session(), Projects(project_name="成都市政项目"))

#增加公司
addOrRecord(ContractDB.session(), Companies(company_name="设计一公司"))

#增加合同
addOrRecord(ContractDB.session(), Contracts(contract_id=createUuid(),contract_name="设计合同", project_id=1, company_id=1))