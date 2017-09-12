#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MySqlAlchemy.EngineCreator import *
from sqlalchemy import *

class Pages(TableBase):
    __tablename__ = "pages_mzitu"

    page_url = Column(String(1000), primary_key=True)
    title = Column(String(20), nullable=False)

class ImageUrls(TableBase):
    __tablename__ = "imageurls_mzitu"

    image_url = Column(String(1000), primary_key=True)
    page_url = Column(String(1000))