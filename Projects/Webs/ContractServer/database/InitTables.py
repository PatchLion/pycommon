from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app.Functions import stringMD5, createUuid
from MySqlAlchemy.DBOperator import *


ContractDB.initTables()

#增加角色表
removeRecords(ContractDB.session(), Role)
admin_role_id = createUuid()
test_role1_id = createUuid()
test_role2_id = createUuid()
addOrRecord(ContractDB.session(), Role(name ="管理员")) #管理员权限
addOrRecord(ContractDB.session(), Role(name ="测试角色1")) #
addOrRecord(ContractDB.session(), Role(name ="测试角色2")) #

#增加用户
removeRecords(ContractDB.session(), User)
addOrRecord(ContractDB.session(), User(user="root", password=stringMD5("root"), name="root"))
addOrRecord(ContractDB.session(), User(user="admin", password=stringMD5("admin"), name="Adminstrator"))
addOrRecord(ContractDB.session(), User(user="simple", password=stringMD5("simple"), name="SimpleLove"))
addOrRecord(ContractDB.session(), User(user="patchlion", password=stringMD5("patchlion"), name="打补丁的狮子"))

#增加项目
removeRecords(ContractDB.session(), Project)
addOrRecord(ContractDB.session(), Project(name="成都市政项目"))

#增加公司
removeRecords(ContractDB.session(), Company)
addOrRecord(ContractDB.session(), Company(name="设计一公司"))
