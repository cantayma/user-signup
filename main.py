import webapp2
import re

header = """
<DOCTYPE! html>
    <head>
        <title>User Signup</title>
    </head>
    <body>
        <h1>User Signup</h1>
        <br>
        <h3>Please fill out the form below to create an account.</h3>
"""
form = """
        <form action="/welcome" method="post">
            <label>
                Username:
                <input type="text" name="username">
            </label>
            <br>
            <label>
                Password:
                <input type="password">
            </label>
            <br>
            <label>
                Verify Password:
                <input type="verify">
            </label>
            <br>
            <label>
                Email (optional):
                <input type="email" name="email">
            </label>
            <br>
            <input type="submit">
        </form>
"""

footer = """
    </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = header + form + footer
        self.response.write(content)

    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        verified_password = self.request.get("verify")
        email = self.request.get("email")

        user_error = """
        Sorry, that's not a valid username.
        Please try again.
        Username must be 3-20 characters long and not include any puctuation
        other than "_" or "-".
        """

        password_error = """
        Oops! Your passwords don't match. Please try again.
        """

        email_error = """
        That's doesn't look like a valid email.
        Please make sure it has an "@" and a "."
        """

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        def valid_username(username):
            if username and USER_RE.match(username):
                return True
            return user_error

        PASS_RE = re.compile(r"^.{3,20}$")
        def valid_password(password):
            if PASS_RE.match(password) and verified_password(password):
                return True
            return password_error

        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        def valid_email(email):
            if EMAIL_RE.match(email):
                return True
            return email_error

        #if all is good, redirect to /welcome
        #if bad then
        #redirect to /

class Welcome(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get()
        self.response.write("Welcome, ")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
