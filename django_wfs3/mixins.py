from rest_framework.response import Response
from rest_framework.decorators import action


class WFS3DescribeModelMixin:
    """
    Describe endpoint for WFS3
    """

    # TODO : see if we need this anyway, as all info is already in wfs3/collections
    def describe(self, request, *args, **kwargs):
        return Response(
            {
                "id": "permit",  # TODO - how can we retrieve prefix from here ?
                "title": "permit",  # TODO - how can we retrieve prefix from here ?
                "description": "?",
                "extent": {
                    "spatial": {"bbox": [[7.01, 50.63, 7.22, 50.78]]},  # TODO - retrieve from the viewset
                },
                "links": [
                    {
                        "href": request.build_absolute_uri("items/"),
                        "rel": "items",
                        "type": "application/geo+json",
                        "title": "permit",  # TODO - how can we retrieve prefix from here ?
                    },
                ],
            }
        )
