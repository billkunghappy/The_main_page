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
from google.appengine.ext import db
import signup
from signup import User_data
from signup import hash_salt
import hashlib
# deliete parent in db
# def blog_key(name='default'):
#     return db.Key.from_path('blogs', name)

def hash_str(s):
    return hashlib.md5(s).hexdigest()
def make_secure_val(s,salt):
    return "%s|%s" % (s, hash_str(s+salt))
def check_secure_val(h,salt):
    val=h.split('|')[0]
    if h==make_secure_val(val,salt):
        return val

class Post(db.Model):
    subject=db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)
    username=db.StringProperty(required=True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'username': self.username}
        return d
#    Last_time=db.DateTimeProperty(auto_now=True)
    # def render(self):
    #     self._render_text =self.content.replace('\n','<br>')
    #     return self.render_str('post.html',p=self) 
class Newpost(BaseHandler):
    def get(self):
        cookie=self.request.cookies.get('user_key')
        user=None
        if cookie:
            user=check_secure_val(cookie,hash_salt)
        if user:
            userkey=db.get(user)
            if userkey:
                userhash=make_secure_val(str(userkey.username),hash_salt)
                self.response.headers.add_header('Set-Cookie','user=%s'%userhash)
                self.render('blog_input.html')
        else:
            
            self.redirect("/Blog")
    def post(self):
        subject=self.request.get("subject")
        content=self.request.get("content")
        name=self.request.cookies.get('user')
        username=check_secure_val(name,hash_salt)
        
        terror=""
        werror=""

        if username:
            if subject!="" and content!="":
                w=Post(subject=subject,content=content,username=username)
                w.put()
                self.redirect('/Blog')
            else:
                if subject=="":
                    terror="You didn't enter the title!"
                if content=="":
                    werror="You didn't enter any word!"
                self.render('blog_input.html',subject=subject,content=content,terror=terror,werror=werror)
        else:
            self.redirect('/Blog')
# class Blog_new(BaseHandler):
#     def get(self):
#         key.db.from_path('post',int(post_id),parent=blog_key)
#         post=db.get(key)
#         if not post:
#             self.error(404)
#             return
#         self.render("blog_new",post=post)

        
class Blog(BaseHandler):
    def get(self):
        posts=db.GqlQuery('select * from Post order by created desc limit 10')
        if self.format == 'html':
            self.render('blog.html',posts=posts)
        else:
            return self.render_json([p.as_dict() for p in posts])
