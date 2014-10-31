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
import random
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env= Environment(loader=FileSystemLoader(template_dir),
                                autoescape=True)
class BaseHandler(webapp2.RequestHandler):
  
    def write(self, *a, **kw):
    	self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render(self, template,**kw):
        self.write(self.render_str(template,**kw))

###############################################################################
class MainHandler(BaseHandler):
    def get(self):
        self.render('main_page.html')
###############################################################################
class FizzBuzz(webapp2.RequestHandler):
    def get(self):
        n=self.request.get("n")
    	n= n and int(n)
        jinja_env= Environment(loader=FileSystemLoader('templates'))
    	template = jinja_env.get_template('FizzBuzz.html')
    	self.response.out.write(template.render(n=n))
###############################################################################
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
###############################################################################
class User_Sing_Up1(BaseHandler):
    def render_front(self,username="",password="",verify="",email="",
                    nameerror="",passworderror="",verifyerror="",emailerror=""):
        self.render('user_sign_up.html',username=username,password=password,verify=verify,email=email,
                    nameerror=nameerror,passworderror=passworderror,verifyerror=verifyerror,emailerror=emailerror)
    def get(self):
        self.render_front()
        
    def post(self):
        a=""
        b=""
        c=""
        d=""
        username=self.request.get("username")
        password=self.request.get("password")
        verify=self.request.get("verify")
        email=self.request.get("email")
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        EML_RE  = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        PWD_RE  = re.compile(r"^.{3,20}$")
        alist=[username,password,verify,email]
        a,b,c,d=self.check(alist,EML_RE,PWD_RE,USER_RE)
        
        if a=="" and b=="" and c=="" and d=="" :
            self.redirect("/Welcome?username="+username)
        else:
            self.render_front(username,password,verify,email,a,b,c,d)
    def check(self,alist,EML_RE,PWD_RE,USER_RE):
        name_wrong=""
        password_wrong=""
        not_verify=""
        email_wrong=""
        if not (USER_RE.match(alist[0])):
            name_wrong="This isn't a valid name"

        if  not (PWD_RE.match(alist[1])):
            password_wrong="This isn't a valid password"
        else:
            if alist[1]!=alist[2]:
                not_verify="Your password didn't match"

        if not (EML_RE.match(alist[3])):
            email_wrong="Your email isn't valid"
        return name_wrong,password_wrong,not_verify,email_wrong

class Welcome(webapp2.RequestHandler):
    def get(self):
        user_check=self.request.cookies.get('user')
        username=(self.request.cookies.get('user')).split('|')[0]
        if user_check:
            user_cookie_check=check_secure_val(user_check)
            if user_cookie_check:
                username=user_cookie_check
            else:
                self.redirect("/User_Sign_Up")

        self.response.out.write("<h1>Welcome,"+username+"!</h1>")
#######################################################################################################

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)
class Post(db.Model):
    subject=db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)
#    Last_time=db.DateTimeProperty(auto_now=True)
    # def render(self):
    #     self._render_text =self.content.replace('\n','<br>')
    #     return self.render_str('post.html',p=self) 
class Newpost(BaseHandler):
    def get(self):
        self.render('blog_input.html')
    def post(self):
        subject=self.request.get("subject")
        content=self.request.get("content")
        terror=""
        werror=""
        if subject!="" and content!="":
            w=Post(parent=blog_key(),subject=subject,content=content)
            w.put()
            self.redirect('/Blog')
        else:
            if subject=="":
                terror="You didn't enter the title!"
            if content=="":
                werror="You didn't enter any word!"
            self.render('blog_input.html',subject=subject,content=content,terror=terror,werror=werror)

class Blog_new(BaseHandler):
    def get(self):
        key.db.from_path('post',int(post_id),parent=blog_key)
        post=db.get(key)
        if not post:
            self.error(404)
            return
        self.render("blog_new",post=post)

        
class Blog(BaseHandler):
    def get(self):
        posts=db.GqlQuery('select * from Post order by created desc limit 10')
        self.render('blog_frontpage.html',posts=posts)
        #self.write(posts.content)
###################################################################################################
def hash_str(s):
    return hashlib.md5(s).hexdigest()
def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))
def check_secure_val(h):
    val=h.split('|')[0]
    if h==make_secure_val(val):
        return val

class Cookies_Visits(BaseHandler):
    def get(self):
        self.response.headers['Content-Type']='text/plain'
        visits=0
        check_visits=self.request.cookies.get('visits')
        #self.response.out.write(check_visits)
        if check_visits:
            cookie_val=check_secure_val(check_visits)
            #self.response.out.write(cookie_val)
            if cookie_val:
                visits=int(cookie_val)
        visits+=1
        new_visits=make_secure_val(str(visits))
        self.response.headers.add_header('Set-Cookie','visits=%s' % new_visits)
        if visits>=1000:
            self.write("You are the best ever!!!")
        else:
            self.write("You've been here %s times !" % visits)
###################################################################################################
class Make_3D(BaseHandler):
    def get(self):
        self.render("threex_test1.html")
###################################################################################################
class User_Sign_Up(BaseHandler):
    def salt():
        return "".join(random.choice(string.letters)for x in xrange(5))
    def add_salt(name):
        return name+salt()
    def get(self):
        self.render("USU_L4.html")
    def post(self):
        username=self.request.get("username")
        self.response.headers['Content-Type']='text/plain'
        user=make_secure_val(str(username))
        self.response.headers.add_header('Set-Cookie','user=%s' % user)
        self.redirect("/Welcome")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/FizzBuzz', FizzBuzz),
    ('/ROT13', ROT13),
    ('/User_Sign_Up1', User_Sing_Up1),
    ('/Welcome', Welcome),
    ('/Blog/newpost',Newpost),
    ('/Blog?',Blog),
    ('/Blog/(\d+)',Blog_new),
    ('/Cookies_Visits',Cookies_Visits),
    ('/3D',Make_3D),
    ('/User_Sign_Up',User_Sign_Up)
], debug=True)
