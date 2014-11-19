#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import os
from jinja2 import Environment, FileSystemLoader
import re
import hashlib
import random,string
import logging
import sys
sys.path.append("python_file")
###############################################################################
import basehandler
from basehandler import BaseHandler
###############################################################################
class MainHandler(BaseHandler):
    def get(self):
        self.render('main_page.html')

        logging.error('djdhvka\n\n\n\n\n\n\ndjidlgvuiha')
###############################################################################
from fizzbuzz import FizzBuzz
###############################################################################
from ROT13 import ROT13
###############################################################################
import signup
from signup import User_Sign_Up
from signup import Login
from signup import Logout
from signup import Welcome
#######################################################################################################
from blog import Post
from blog import Newpost
from blog import Blog
###################################################################################################
class Make_3D(BaseHandler):
    def get(self):
        self.render("threex_test1.html")
###################################################################################################
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/FizzBuzz', FizzBuzz),
    ('/ROT13', ROT13),
    # ('/User_Sign_Up1', User_Sing_Up1),
    ('/welcome', Welcome),
    ('/Blog/newpost',Newpost),
    ('/Blog?(?:.json)?',Blog),
    # ('/Blog/(\d+)',Blog_new),
    # ('/Cookies_Visits',Cookies_Visits),
    ('/3D',Make_3D),
    ('/signup',User_Sign_Up),
    ('/login',Login),
    ('/logout',Logout)
], debug=True)
