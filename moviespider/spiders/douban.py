# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
import hashlib
from scrapy import Request
from moviespider.items import MoviespiderItem


class ExampleSpider(scrapy.Spider):
    name = 'douban'
    # sorts = ['R', 'S', 'T']
    sorts = ['R']
    start_url = 'https://movie.douban.com/j/new_search_subjects?sort={0}&range=0,10&tags=电影&start={1}'

    def start_requests(self):
        for sort in self.sorts:
            for start in range(0, 500, 20):
            # for start in range(660, 9980, 20):
                url = self.start_url.format(sort, start)
                yield Request(url, self.parse, meta={
                })

    def parse(self, response):
        self.log(response.url, level=logging.INFO)
        for data in json.loads(response.text)['data']:
            detail_url = data['url']
            self.log(detail_url, level=logging.INFO)
            yield Request(detail_url, self.parse_detail, meta={
                'list_data': data
            })

    def parse_detail(self, response):
        data = response.meta['list_data']
        info = response.xpath('//*[@id="info"]').extract_first()
        try:
            info_str = re.compile(r'<.*?>', flags=re.M).sub('', info)
        except Exception as e:
            self.log(e, level=logging.INFO)
        # self.log(info_str, level=logging.INFO)
        # print (data['directors'],'====','／'.join(data['directors']))
        item = MoviespiderItem()
        item['id'] = hashlib.md5(response.url.encode()).hexdigest()
        item['directors'] = '／'.join(data['directors'])
        item['rate'] = data['rate']
        item['title'] = data['title']
        item['origin'] = '豆瓣爬虫'
        item['casts'] = '/'.join(data['casts'])
        item['cover'] = data['cover']
        item['movie_id'] = data['id']
        item['link'] = data['url']
        item['screenwriter'] = ''.join(re.compile(r'编剧:(.*)').findall(info_str)).strip()
        item['category'] = ''.join(re.compile(r'类型:(.*)').findall(info_str)).strip()
        item['contury'] = ''.join(re.compile(r'制片国家/地区:(.*)').findall(info_str)).strip()
        item['language'] = ''.join(re.compile(r'语言:(.*)').findall(info_str)).strip()
        item['screenwriter'] = ''.join(re.compile(r'类型:(.*)').findall(info_str)).strip()
        item['onview_date'] = ''.join(re.compile(r'上映日期:(.*)').findall(info_str)).strip()
        item['duration'] = ''.join(re.compile(r'片长:(.*)').findall(info_str)).strip()
        item['alias'] = ''.join(re.compile(r'又名:(.*)').findall(info_str)).strip()
        item['imdb_id'] = ''.join(re.compile(r'IMDb链接:(.*)').findall(info_str)).strip()
        item['status'] = '0'

        # 获取热门评论
        comments_wrapper = response.xpath('//*[@id="hot-comments"]/div/div')
        comments = []
        for comment_wrapper in comments_wrapper:
            rate_str = comment_wrapper.xpath('descendant-or-self::h3/span[2]/span[contains(@class,"rating")]/@class').extract_first()
            comment = {
                'author': comment_wrapper.xpath('descendant-or-self::h3/span[2]/a/text()').extract_first().strip(),
                'author_profile': comment_wrapper.xpath('descendant-or-self::h3/span[2]/a/@href').extract_first().strip(),
                'rate': ''.join(re.findall(r'allstar(\d+) rating', rate_str)),
                'content': comment_wrapper.xpath('descendant-or-self::p/text()').extract_first().strip(),
                'created_at': comment_wrapper.xpath('descendant-or-self::h3/span[2]/span[contains(@class,"comment-time")]/text()').extract_first().strip()
            }
            self.log(comments, level=logging.DEBUG)
            comments.append(comment)
        item['comments'] = comments
        detail = response.xpath('//*[@id="link-report"]').extract_first()
        try:
            item['imdb_link'] = re.compile('<a href="(.*?)".*?>.*?' + item['imdb_id']).findall(info)[0]
            item['detail'] = re.compile(r'<.*?>', flags=re.M).sub('', detail).strip()
        except Exception as e:
            print(e)

        yield item
        # self.log(data['url'], level=logging.INFO)
        # self.log(response.url, level=logging.INFO)
