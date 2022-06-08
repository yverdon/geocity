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

@app.route("/", methods=['POST'])
def pdf():

    url = os.environ["WEB_ROOT_URL"] + request.form['url']
    token = request.form['token']



    def fetcher(url):
        print(f"FETCHING {url}", file=sys.stdout, flush=True)
        if url.startswith(os.environ["WEB_ROOT_URL"]):
            # This is an internal call, we need to authenticate it with the token
            print("abc", flush=True)
            req = Request(url)
            req.add_header('Authorization', f'Token {token}')
            return {"file_obj": urlopen(req)}
        return default_url_fetcher(url)


    buffer = io.BytesIO()
    wp = weasyprint.HTML(url=url, url_fetcher=fetcher)
    wp.write_pdf(buffer)
    buffer.seek(io.SEEK_SET)
    return send_file(buffer, mimetype="application/pdf")
