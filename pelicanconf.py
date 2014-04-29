#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Mouer'
SITENAME = u'Morse Code'
SITE_URL = 'http://mouer.me'

PATH = 'content'
THEME = "myTheme"

# atom.xml
FEED_ALL_ATOM = 'feeds/atom.xml'

# 时区
TIMEZONE = 'Asia/Shanghai'
LOCALE = ('en_US')

# 禁用功能
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''

# 图片
STATIC_PATHS = [u'pic', u'extra']
EXTRA_PATH_METADATA = {
        u'extra/robots.txt': {'path': u'robots.txt'},
        u'extra/favicon.ico': {'path': u'favicon.ico'},
        u'extra/CNAME': {'path': u'CNAME'},
}


# 重写url
ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"
SITEMAP_SAVE_AS = 'sitemap.xml'

# add sitemap
DIRECT_TEMPLATES = ('index', 'tags', 'categories', 'archives', 'sitemap')

# 评论
DISQUS_SITENAME = u'mouer73'
