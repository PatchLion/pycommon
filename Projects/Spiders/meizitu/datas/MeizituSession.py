from MySqlAlchemy.EngineCreator import *
from Projects.Spiders.meizitu.meizitu.settings import *
from Projects.Spiders.meizitu.datas.tables import *
import os

meizituSession = createEngine("sqlite:///" + DBFILE, not os.path.exists(DBFILE))