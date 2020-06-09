from django.shortcuts import redirect


def redirect_permit(request):
    response = redirect('/permit-request')
    return response
