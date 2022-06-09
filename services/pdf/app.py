from socketserver import ThreadingUnixDatagramServer
from flask import Flask
from flask import request
from flask import send_file
import weasyprint
import requests
import io
import os
import sys
from urllib.request import urlopen
from urllib.request import Request, urlopen

from weasyprint import HTML, default_url_fetcher

app = Flask(__name__)


@app.route("/", methods=["POST"])
def pdf():

    url = os.environ["WEB_ROOT_URL"] + request.form["url"]
    token = request.form["token"]

    # Custom URL fetcher that adds the authentication header for internal
    def fetcher(url):
        if url.startswith(os.environ["WEB_ROOT_URL"]):
            req = Request(url)
            req.add_header("Authorization", f"Token {token}")
            return {"file_obj": urlopen(req)}
        return default_url_fetcher(url)

    buffer = io.BytesIO()
    wp = weasyprint.HTML(url=url, url_fetcher=fetcher)
    wp.write_pdf(buffer)
    buffer.seek(io.SEEK_SET)
    return send_file(buffer, mimetype="application/pdf")
