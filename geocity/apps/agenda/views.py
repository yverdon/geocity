from django.shortcuts import render
from django.urls import reverse


def agenda(request):
    api_root = reverse("api-root")[:-1]
    context = {
        "api_root": api_root,
    }

    return render(
        request,
        "agenda/agenda.html",
        context,
    )


def agenda_sports(request):
    api_root = reverse("api-root")[:-1]
    context = {
        "api_root": api_root,
    }

    return render(
        request,
        "agenda/agenda_sports.html",
        context,
    )


def agenda_culture(request):
    api_root = reverse("api-root")[:-1]
    context = {
        "api_root": api_root,
    }

    return render(
        request,
        "agenda/agenda_culture.html",
        context,
    )
