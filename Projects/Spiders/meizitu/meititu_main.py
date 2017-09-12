from MySqlAlchemy import *
from Projects.Spiders.meizitu.datas.tables import *
from Projects.Spiders.meizitu.datas.MeizituSession import meizituSession

rs = records(meizituSession, ImageUrls)

for r in rs:
    print(r.page_url, r.image_url)

print("Record count = ", len(rs))