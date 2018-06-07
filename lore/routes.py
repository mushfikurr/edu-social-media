from lore import app

@app.route("/")
@app.route("/home")
def home():
    """
    Endpoint for homepage.
    """
    return "<h1>This is the homepage.</h1>"

@app.route("/about")
def about():
    """
    Endpoint for about page.
    """
    return "<h1>This is the about page.</h1>"