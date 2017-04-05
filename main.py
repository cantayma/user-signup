import webapp2

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
        <form>
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
                <input type="password">
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
        #error checkig here
        #if good then
        #redirect to /welcome

class Welcome(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get()
        self.response.write("Welcome, ")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
