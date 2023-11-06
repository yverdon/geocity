from django.shortcuts import render


def agenda(request):
    return render(
        request,
        "agenda/agenda.html",
        {},
    )
