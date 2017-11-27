# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MoviespiderItem(scrapy.Item):
    # define the fields for your item here like:
    movie_id = Field()
    directors = Field()
    origin = Field()
    title = Field()
    category = Field()
    link = Field()
    cover = Field()
    rate = Field()
    casts = Field()
    status = Field()
    detail = Field()
    screenwriter = Field()
    language = Field()
    contury = Field()
    onview_date = Field()
    duration = Field()
    alias = Field()
    imdb_id = Field()
    imdb_link = Field()
