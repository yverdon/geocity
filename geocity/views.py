from django.shortcuts import redirect


# Redirect "permit-requests" URLs to "submissions" URLs. Will be deprecated in 3.0
def legacy_urls_redirect(request):
    new_url = request.path.replace("permit-requests/", "submissions/")

    if request.META["QUERY_STRING"]:
        new_url = f'{new_url}?{request.META["QUERY_STRING"]}'

    return redirect(new_url)
