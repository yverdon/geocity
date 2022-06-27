import argparse
from urllib.request import Request, urlopen

import weasyprint
from weasyprint import default_url_fetcher

INTERNAL_WEB_ROOT_URL = "http://web:9000"


def export(args):

    url = args.url
    output_path = args.output_path
    token = args.token

    print(f"Exporting {url=} {output_path=} {token=}")

    # Custom URL fetcher that adds the authentication header for internal
    def fetcher(url):
        print(f"Fetching {url[:80]}..." if len(url) > 80 else f"Fetching {url}")
        if url.startswith(INTERNAL_WEB_ROOT_URL):
            req = Request(url)
            req.add_header("Authorization", f"Token {token}")
            return {"file_obj": urlopen(req)}
        return default_url_fetcher(url)

    wp = weasyprint.HTML(
        url=url,
        base_url=INTERNAL_WEB_ROOT_URL,
        url_fetcher=fetcher,
    )
    wp.write_pdf(output_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="url to transform to PDF")
    parser.add_argument("output_path", type=str, help="path to output")
    parser.add_argument("token", type=str)

    export(parser.parse_args())
