import argparse
from urllib.request import Request, urlopen

import weasyprint
from weasyprint import default_url_fetcher

INTERNAL_WEB_ROOT_URL = "http://web:9000"


def export(args):

    input_path = args.input_path
    output_path = args.output_path
    token = args.token

    print(f"Exporting {input_path=} {output_path=} {token=}")

    # Custom URL fetcher that adds the authentication header for internal
    def fetcher(url):
        print(f"Fetching {url[:80]}..." if len(url) > 80 else f"Fetching {url}")
        if url.startswith(INTERNAL_WEB_ROOT_URL):
            req = Request(url)
            req.add_header("Authorization", f"Token {token}")
            return {"file_obj": urlopen(req)}
        return default_url_fetcher(url)

    wp = weasyprint.HTML(
        filename=input_path,
        base_url=INTERNAL_WEB_ROOT_URL,
        url_fetcher=fetcher,
    )
    wp.write_pdf(output_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str, help="path to html input file")
    parser.add_argument("output_path", type=str, help="path to output")
    parser.add_argument("token", type=str)

    export(parser.parse_args())
