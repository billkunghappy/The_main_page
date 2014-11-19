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
            self.redirect("/welcome?username="+username)
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

################################################################################
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