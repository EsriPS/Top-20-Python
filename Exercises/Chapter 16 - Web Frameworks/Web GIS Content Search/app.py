import os
import sys
import urllib.parse
import secrets
from datetime import datetime
from arcgis.gis import GIS

from flask import Flask, session, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms.fields import DateField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional

from gis_inventory import items_search


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static"),
)

# Registering the extensions
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

app.secret_key = secrets.token_urlsafe(16)
app.config.from_object(__name__)


class TokenForm(FlaskForm):
    url = StringField(
        "ArcGIS Online or Portal URL", validators=[DataRequired(), Length(max=255)]
    )
    username = StringField("Username", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=255)])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    owner = StringField("Owner")
    group = StringField("Group")
    tag = StringField("Tag")
    content_status = StringField("Content Status")
    created_from = DateField("Created From", default=None, validators=[Optional()])
    created_to = DateField("Created To", default=None, validators=[Optional()])
    modified_from = DateField("Modified From", default=None, validators=[Optional()])
    modified_to = DateField("Modified To", default=None, validators=[Optional()])
    output_path = StringField("Output Path")
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Renders the index page of the web application.

    If the user is not authenticated, it redirects to the "get_token" route.
    The function handles both GET and POST requests.

    GET Request:
    - Repopulates the form from the previous search, if any.
    - Parses the query string parameters and converts date strings to datetime objects.
    - Renders the index.html template with the query string, search form, search query, and current portal.

    POST Request:
    - Validates the search form.
    - Constructs the search query parameters from the form data.
    - Redirects to the index route with the updated query string.

    Returns:
    - If the request is a GET request, it returns the rendered index.html template.
    - If the request is a POST request, it redirects to the index route with the updated query string.
    """

    # Check if the user is authenticated
    if "token" not in session:
        return redirect(url_for("get_token"))

    # Repopulate the form from the previous search
    query_string = request.args.get("query_string", "/api/data?", type=str)
    unparsed_query = urllib.parse.parse_qs(query_string.replace("/api/data?", ""))
    unparsed_query = {key: value[0] for key, value in unparsed_query.items()}

    # Convert the date strings to datetime objects
    if unparsed_query.get("created_from", None):
        unparsed_query["created_from"] = datetime.strptime(
            unparsed_query["created_from"], "%Y-%m-%d"
        )

    if unparsed_query.get("created_to", None):
        unparsed_query["created_to"] = datetime.strptime(
            unparsed_query["created_to"], "%Y-%m-%d"
        )

    if unparsed_query.get("modified_from", None):
        unparsed_query["modified_from"] = datetime.strptime(
            unparsed_query["modified_from"], "%Y-%m-%d"
        )

    if unparsed_query.get("modified_to", None):
        unparsed_query["modified_to"] = datetime.strptime(
            unparsed_query["modified_to"], "%Y-%m-%d"
        )

    # Create the search form with default values
    search_form = SearchForm(**unparsed_query)

    # Handle the POST request
    if search_form.validate_on_submit():

        # Construct the search query parameters
        search_query_params = {
            "owner": search_form.owner.data,
            "group": search_form.group.data,
            "tag": search_form.tag.data,
            "content_status": search_form.content_status.data,
            "created_from": search_form.created_from.data,
            "created_to": search_form.created_to.data,
            "modified_from": search_form.modified_from.data,
            "modified_to": search_form.modified_to.data,
            "output_path": search_form.output_path.data,
        }

        # Encode the search query parameters
        search_query = urllib.parse.urlencode(
            {
                key: value
                for key, value in search_query_params.items()
                if value is not None
            }
        )

        # Redirect to the index route with the updated query string
        return redirect(
            url_for(
                "index",
                query_string=f"/api/data?{search_query}",
            ),
        )

    return render_template(
        "index.html",
        query_string=query_string,
        search_form=search_form,
        search_query=request.args.get("search_query", None, type=str),
        url=session["url"],
        current_portal=session.get("url", None),
    )


@app.route("/get_token", methods=["GET", "POST"])
def get_token(message: str = None):
    """
    Route handler for the '/get_token' endpoint.
    Handles GET and POST requests to retrieve a token for the GIS.

    Args:
        message (str, optional): A message to display on the page. Defaults to None.

    Returns:
        Response: A redirect response to the 'index' endpoint or a rendered template for 'get_token.html'.
    """

    # Create a token form
    token_form = TokenForm()

    # Handle the POST request
    if token_form.validate_on_submit():

        # Obtain and store the token and URL in the session
        session["token"] = GIS(
            username=token_form.username.data,
            password=token_form.password.data,
            url=token_form.url.data,
        )._con.token
        session["url"] = token_form.url.data
        return redirect(url_for("index"))

    return render_template(
        "get_token.html",
        message=message,
        token_form=token_form,
        current_portal=session.get("url", None),
    )


@app.route("/logout")
def logout():
    """
    Logs out the user by removing the session token and URL.

    Returns:
        A redirect response to the "get_token" route with a logout message.
    """
    session.pop("token", None)
    session.pop("url", None)
    return redirect(url_for("get_token", message="You have been logged out."))


@app.route("/api/data")
def data():
    """
    Retrieves data based on specified search parameters.

    Args:
        search (str): The search string to append to the existing search.
        owner (str): The owner of the content.
        group (str): The group of the content.
        tag (str): The tag associated with the content.
        content_status (str): The status of the content.
        created_from (str): The starting date for content creation.
        created_to (str): The ending date for content creation.
        modified_from (str): The starting date for content modification.
        modified_to (str): The ending date for content modification.
        output_path (str): The path to save the output.

    Returns:
        dict: A dictionary containing the retrieved data.

    Raises:
        None

    """

    # Get the search parameters
    append_search_string = request.args.get("search", None, type=str)
    owner = request.args.get("owner", None, type=str)
    group = request.args.get("group", None, type=str)
    tag = request.args.get("tag", None, type=str)
    content_status = request.args.get("content_status", None, type=str)
    created_from = request.args.get("created_from", None, type=str)
    created_to = request.args.get("created_to", None, type=str)
    modified_from = request.args.get("modified_from", None, type=str)
    modified_to = request.args.get("modified_to", None, type=str)
    output_path = request.args.get("output_path", None, type=str)

    # Convert the date strings to datetime objects
    if created_from:
        created_from = datetime.strptime(created_from, "%Y-%m-%d")

    if created_to:
        created_to = datetime.strptime(created_to, "%Y-%m-%d")

    if modified_from:
        modified_from = datetime.strptime(modified_from, "%Y-%m-%d")

    if modified_to:
        modified_to = datetime.strptime(modified_to, "%Y-%m-%d")

    # Get the search results
    results = items_search(
        gis=GIS(url=session["url"], token=session["token"]),
        append_search_string=append_search_string,
        owner=owner,
        group=group,
        tag=tag,
        content_status=content_status,
        created_from=created_from,
        created_to=created_to,
        modified_from=modified_from,
        modified_to=modified_to,
        output_path=output_path,
    )

    # Return the results
    return {
        "data": results["results"],
    }


if __name__ == "__main__":
    app.run()
