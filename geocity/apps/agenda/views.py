from django.shortcuts import render


def agenda(request):
    return render(
        request,
        "agenda/agenda.html",
        {},
    )


def agenda_sports(request):
    return render(
        request,
        "agenda/agenda_sports.html",
        {},
    )


def agenda_culture(request):
    return render(
        request,
        "agenda/agenda_culture.html",
        {},
    )
