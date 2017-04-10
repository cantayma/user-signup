import webapp2
import re
import cgi


header = """
<DOCTYPE! html>
    <head>
        <title>User Signup</title>
    </head>
    <body>
        <h1>User Signup</h1>
        <h3>Please fill out the form below to create an account.</h3>
"""

form = """
        <form method="post">
            <label>
                Username:
                <input type="text" name="username">
                <span style="color:purple">%(username_error)s</span>
            </label>
            <br>
            <label>
                Password:
                <input type="password" name="password">
                <span style="color:purple">%(valid_password_error)s</span>
            </label>
            <br>
            <label>
                Verify Password:
                <input type="password" name="verify">
                <span style="color:purple">%(password_match_error)s</span>
            </label>
            <br>
            <label>
                Email (optional):
                <input type="email" name="email">
                <span style="color:purple">%(email_error)s</span>
            </label>
            <br>
            <br>
            <input type="submit">
        </form>

"""

footer = """
    </body>
</html>
"""


class MainHandler(webapp2.RequestHandler):

    def write_form(self, username_error_msg="", valid_password_error_msg="", password_match_error_msg="", email_error_msg=""):
        self.response.write(
            header
            + form % {
            "username_error":username_error_msg,
            "valid_password_error":valid_password_error_msg,
            "password_match_error":password_match_error_msg,
            "email_error":email_error_msg
            } + footer)

    def get(self):
        self.write_form()

    def post(self):
        username = cgi.escape(self.request.get("username"), quote=True)
        password = cgi.escape(self.request.get("password"), quote=True)
        verify = cgi.escape(self.request.get("verify"), quote=True)
        email = cgi.escape(self.request.get("email"), quote=True)

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        def validate_username(username):
            if username and USER_RE.match(username):
                return True
            return False

        PASS_RE = re.compile(r"^.{3,20}$")
        def validate_password(password):
            if PASS_RE.match(password):
                return True
            return False

        def match_password(password, verify):
            if password == verify:
                return True
            return False

        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        def validate_email(email):
            if EMAIL_RE.match(email) or email=="":
                return True
            return False

        valid_username = validate_username(username)
        valid_password = validate_password(password)
        valid_verify = match_password(password, verify)
        valid_email = validate_email(email)

        username_error_msg = """
        Sorry, that's not a valid username. Please make sure it's 3-20 characters
        and has at least one "_" or "-" and a number.
        """
        valid_password_error_msg = """
        Your password must be between 3-20 characters and may have a "."
        """
        password_match_error_msg = """
        Oops! Your passwords don't match. Please try again.
        """
        email_error_msg = """
        That's doesn't look like a valid email.
        Please make sure it has an "@" and a "."
        """
        if valid_username and valid_password and valid_verify and valid_email:
            self.redirect("/welcome?username=" + username)

        if not valid_username:
            username_error_msg = username_error_msg
        elif not valid_password or valid_verify:
            username_error_msg = ""
            valid_password_error_msg = valid_password_error_msg
            password_match_error_msg = password_match_error_msg

        if not valid_password:
            valid_password_error_msg = valid_password_error_msg
        elif not valid_username or valid_verify:
            username_error_msg = username_error_msg
            valid_password_error_msg = ""
            password_match_error_msg = password_match_error_msg

        if not valid_verify:
            password_match_error_msg = password_match_error_msg
        elif not valid_username or valid_password:
            username_error_msg = username_error_msg
            valid_password_error_msg = valid_password_error_msg
            password_match_error_msg = ""

        if not valid_email:
            email_error_msg = email_error_msg
        elif not valid_username or valid_password or valid_verify:
            username_error_msg = username_error_msg
            valid_password_error_msg = valid_password_error_msg
            password_match_error_msg = password_match_error_msg
            email_error_msg = ""

        self.write_form(
            username_error_msg,
            valid_password_error_msg,
            password_match_error_msg,
            email_error_msg)



class Welcome(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get("username")
        self.response.write("Welcome, " + user_name + "!")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
