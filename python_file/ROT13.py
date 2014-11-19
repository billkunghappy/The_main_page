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
import basehandler 
from basehandler import BaseHandler

class ROT13(BaseHandler):
    def get(self):
        self.render('ROT13.html',text=self.check(self.request.get("text")))
    def check(self,words):
        result=""
        for a in words:
            if ord(a) not in range(ord("a"),ord("z")+1) and ord(a) not in range(ord("A"),ord("Z")+1):
                if a=="<":
                    a="&lt;"
                elif a==">":
                    a="&gt;"
                elif a=='"':
                    a="&quot;"
                elif a=="&":
                    a="&amp;"
                else:
                    a=a
                result=result+a
            else:
                if a==a.upper():
                    result=result+chr((ord(a)-ord("A")+13)%26+ord("A"))
                else:    
                    result=result+chr((ord(a)-ord("a")+13)%26+ord("a"))
        return result