#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import os
from jinja2 import Environment, FileSystemLoader
import re
import hashlib
import random,string
import logging

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env= Environment(loader=FileSystemLoader(template_dir),
                                autoescape=True)
class BaseHandler(webapp2.RequestHandler):
    def initialize(self,*a, **kw):
        webapp2.RequestHandler.initialize(self,*a, **kw)
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'
        
    def write(self, *a, **kw):
    	self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render(self, template,**kw):
        self.write(self.render_str(template,**kw))
    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)