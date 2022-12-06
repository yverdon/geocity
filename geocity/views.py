from django.conf import settings
from django.shortcuts import redirect


# Redirect "permit-requests" URLs to "submissions" URLs. Will be deprecated in 3.0
def legacy_urls_redirect(request):

    new_url = f'submissions{request.path.split("permit-requests")[1]}'

    if settings.PREFIX_URL:
        new_url = f"{settings.PREFIX_URL}{new_url}"

    if request.META["QUERY_STRING"]:
        new_url = f'{new_url}?{request.META["QUERY_STRING"]}'

    new_url = f"/{new_url}"

    return redirect(new_url)
