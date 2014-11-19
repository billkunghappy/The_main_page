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
from jinja2 import Environment, FileSystemLoader

class FizzBuzz(webapp2.RequestHandler):
    def get(self):
        n=self.request.get("n")
    	n= n and int(n)
        jinja_env= Environment(loader=FileSystemLoader('templates'))
    	template = jinja_env.get_template('FizzBuzz.html')
    	self.response.out.write(template.render(n=n))