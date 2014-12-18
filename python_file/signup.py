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
import basehandler 
from basehandler import BaseHandler
import random,string
from google.appengine.ext import db
import hashlib

def hash_str(s):
    return hashlib.md5(s).hexdigest()
def make_secure_val(s,salt):
    return "%s|%s" % (s, hash_str(s+salt))
def check_secure_val(h,salt):
    val=h.split('|')[0]
    if h==make_secure_val(val,salt):
        return val


def salt():
    return "".join(random.choice(string.letters)for x in xrange(5))
def add_salt(name):
    salt=salt()
    return "%s,%s"%(name,salt)
def make_pw_hash(pw):
    pwsalt=salt()
    hash_pw=hashlib.md5(pw+pwsalt).hexdigest()
    a="%s,%s"%(pwsalt,hash_pw)
    return a
def check_secure_pw(pw,pw_hash):
    salt=pw_hash.split(',')[0]
    check_pw=hashlib.md5(pw+salt).hexdigest()
    a="%s,%s"%(salt,check_pw)
    if pw_hash==a:
        return True

hash_salt=salt()

class User_data(db.Model):
    username=db.StringProperty(required=True)
    password=db.StringProperty(required=True)
    email=db.StringProperty
    @classmethod
    def by_name(cls, name):
        u = User_data.all().filter('username =', name).get()
        return u
    @classmethod
    def login(cls, name,password):
        u=cls.by_name(name)
        if u and check_secure_pw(password,u.password):
            return u
        else:
            return False


class User_Sign_Up(BaseHandler):
    
    def get(self):
        self.render("USU_L4.html")
    def post(self):
        username=self.request.get("username")
        password=self.request.get("password")
        vpassword=self.request.get("verify")
        email=self.request.get("email")
        usererror=""
        verror=""
        user_exist= User_data.by_name(username)
        

        if password ==vpassword and user_exist==None:
            self.response.headers['Content-Type']='text/plain'
            user=make_secure_val(str(username),hash_salt)
            data_user_put=User_data(username=username,password=make_pw_hash(password),email=email)
            data_user_put.put()
            datakey=data_user_put
            
            userkey=make_secure_val(str(datakey.key()),hash_salt)
            self.response.headers.add_header('Set-Cookie','user_key=%s' % userkey)

            self.redirect("/welcome")
        else:
            if password!=vpassword:
                verror="Your input didn't varify the password above!"
            if user_exist!=None:
                usererror="This user is already exist!"

            self.render("USU_L4.html",verror=verror,usererror=usererror
                ,username=username,email=email)
            verror=""
            usererror=""
###################################################################################################
class Login(BaseHandler):
    def check_already_login(self):
        cookie=self.request.cookies.get('user_key')
        if cookie:
            return None
        else:
            return True

    def get(self):
        self.render('login.html')
    def post(self):
        already=self.check_already_login()
        if already:
            username=self.request.get("username")
            pw=self.request.get('password')
            success=User_data.login(username,pw)
            error=""
            if success:
                self.response.headers['Content-Type']='text/plain'
                userkey=make_secure_val(str(success.key()),hash_salt)
                self.response.headers.add_header('Set-Cookie','user_key=%s' % userkey)
                self.redirect("/welcome")
            else:
                error="Invalid log in!!"
                self.render("login.html",error=error)
        # already log in
        self.redirect("/Blog")

###################################################################################################
class Logout(BaseHandler):
    def get(self):
        self.response.headers['Content-Type']='text/plain'
        self.response.headers.add_header('Set-Cookie','user_key=;')
        self.redirect("/")
###################################################################################################
class Welcome(BaseHandler):
    def get(self):
        cookie=self.request.cookies.get('user_key')
        user=None
        if cookie:
            user=check_secure_val(cookie,hash_salt)
        if user:
            user=db.get(user)
            if user:
                self.render("welcome.html",username=user.username)

        else:
            self.redirect("/signup")