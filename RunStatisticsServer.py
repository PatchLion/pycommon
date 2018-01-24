from PLDatabase import DBInstance
from PLStatistics import runStatisticsApp

DBConnectionString = "mssql+pymssql://sa:Root123456@127.0.0.1:2796/Statistics?charset=utf8"
if __name__ == "__main__":
    DBInstance.resetConnection(DBConnectionString)
    DBInstance.initTables()
    runStatisticsApp()