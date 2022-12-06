from django.shortcuts import redirect


# Redirect "permit-requests" URLs to "submissions" URLs. Will be deprecated in 4.0
def legacy_urls_redirect(request):

    new_url = f'/submissions{request.path.split("permit-requests")[1]}?{request.META["QUERY_STRING"]}'
    return redirect(new_url)