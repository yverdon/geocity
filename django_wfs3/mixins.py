from rest_framework.response import Response
from rest_framework.decorators import action


class WFS3DescribeModelMixin:
    """
    Describe endpoint for WFS3
    """

    def describe(self, request, *args, **kwargs):
        return Response(
            {
                "id": "permit",  # TODO - how can we retrieve prefix from here ?
                "title": "permit",  # TODO - how can we retrieve prefix from here ?
                "description": "?",
                "extent": {
                    "spatial": {"bbox": [[7.01, 50.63, 7.22, 50.78]]},
                    "temporal": {"interval": [["2010-02-15T12:34:56Z", None]]},
                },
                "links": [
                    {
                        "href": request.build_absolute_uri("items/"),
                        "rel": "items",
                        "type": "application/geo+json",
                        "title": "permit",  # TODO - how can we retrieve prefix from here ?
                    },
                    # {
                    #     "href": "http://data.example.org/collections/buildings/items.html",
                    #     "rel": "items",
                    #     "type": "text/html",
                    #     "title": "Buildings",
                    # },
                    # {
                    #     "href": "https://creativecommons.org/publicdomain/zero/1.0/",
                    #     "rel": "license",
                    #     "type": "text/html",
                    #     "title": "CC0-1.0",
                    # },
                    # {
                    #     "href": "https://creativecommons.org/publicdomain/zero/1.0/rdf",
                    #     "rel": "license",
                    #     "type": "application/rdf+xml",
                    #     "title": "CC0-1.0",
                    # },
                ],
            }
        )
