# Django WFS3

This Django app implements an OGC Services API (a.k.a. WFS3) for Django.

It provides a Django Rest Framework (DRF) specific router to which you can
regsiter your Viewsets, and thus benefit from all DRF's features (permissions,
serialization, authentication, etc.).

## Usage

Add this to your `urls.py` :

Register your viewset in the wfs3 router
```python

from django_wfs3.urls import wfs3_router
from .viewsets import MyModelViewSet

wfs3_router.register(r"permits", MyModelViewSet, "permits")
```

Add the router to your `urls.py`
```python
urlpatterns += [
    path("wfs3/", include(django_wfs3.urls))
]
```

## Roadmap / status

This is probably still relatively far from a full OGC Services API implementation and currently only aims to support read-only view from QGIS.

This app will as some point be factored out
into a reusable Django library.
