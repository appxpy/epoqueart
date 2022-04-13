import datetime
import logging
import re
import traceback
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.utils.html import escape

from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict

from django.views.decorators.csrf import csrf_exempt

from django.template.loader import render_to_string

from django.db.models import Q, Max, Min
from django.db.models import Value as V
from django.db.models.functions import Concat

from .models import (
    Country,
    City,
    Currency,
    Gallery,
    Author,
    Artwork_Type,
    Artwork_Status,
    Artwork,
    Event,
)
from accounts.models import CustomUser


def get_base_response():
    return {"message": None, "status": 0, "payload": {}}


def dev(request, *args, **kwargs):
    return render(request, "main/errors/in-development.html")


def handler404(request, *args, **kwargs):
    return render(request, "main/errors/404.html", status=404)


def handler500(request, *args, **kwargs):
    logging.error(traceback.format_exc())
    return render(request, "main/errors/500.html", status=500)


def handler401(request, *args, **kwargs):
    return render(request, "main/errors/401.html", status=401)


def handler400(request, *args, **kwargs):
    return render(request, "main/errors/400.html", status=400)


def handler403(request, *args, **kwargs):
    return render(request, "main/errors/403.html", status=403)


def home(request):
    context = {
        "events": Event.objects.filter(
            date__gt=datetime.date.today() - datetime.timedelta(days=7)
        ).reverse(),
        "artworks": Artwork.objects.all(),
    }
    return render(request, "main/pages/home.html", context)


def about(request):
    return render(request, "main/pages/about.html")


def artists(request):
    context = {"artists": Author.objects.all()}
    return render(request, "main/pages/artists.html", context)


def artist(request, slug):
    author = Author.objects.filter(slug=slug).first()
    if author:
        context = {"artist": author}
        return render(request, "main/pages/artist.html", context)
    else:
        return handler404(request)


def collection(request):
    return render(request, "main/pages/collection.html")


def interior(request):
    return render(request, "main/pages/interior.html")


def on_demand(request):
    return render(request, "main/pages/on-demand.html")


def gallery(request):
    try:
        price__max, price__min = Artwork.objects.aggregate(
            Max("price"), Min("price")
        ).values()
        year__max, year__min = (
            i.year for i in Artwork.objects.aggregate(Max("date"), Min("date")).values()
        )
    except Exception:
        price__max, price__min = (0, 1)
        year__max, year__min = (0, 1)

    pid = request.GET.get("pid", False)
    aid = request.GET.get("aid", False)

    f = request.GET.get("f", False)

    ps = request.GET.get("ps", price__min)
    pe = request.GET.get("pe", price__max)

    ys = request.GET.get("ys", year__min)
    ye = request.GET.get("ye", year__max)

    price__min__value, price__max__value = ps, pe
    year__min__value, year__max__value = ys, ye

    nft = request.GET.get("nft", None)

    if pid and pid.isdigit():
        artworks = Artwork.objects.filter(id=pid)

    elif aid and aid.isdigit():
        artworks = Artwork.objects.filter(author__id=aid)

    elif f:
        _available = Q(status__artwork_is_available=True)

        _nft = Q(is_nft_linked=bool(nft)) if nft is not None else ~Q(pk__in=[])

        if ps.isdigit() and pe.isdigit() and ys.isdigit() and ye.isdigit():
            artworks = Artwork.objects.filter(
                Q(price__range=[int(ps), int(pe)])
                & Q(
                    date__range=[
                        datetime.date(int(ys), 1, 1),
                        datetime.date(int(ye), 12, 31),
                    ]
                )
                & _available
                & _nft
            )

    else:
        artworks = Artwork.objects.all()

    artworks = artworks.filter(Q(status__artwork_is_available=True))
    return render(
        request,
        "main/gallery.html",
        {
            "artworks": artworks,
            "price__max": price__max,
            "price__min": price__min,
            "price__min__value": price__min__value,
            "price__max__value": price__max__value,
            "year__max": year__max,
            "year__min": year__min,
            "year__min__value": year__min__value,
            "year__max__value": year__max__value,
            "nft": bool(nft),
        },
    )


def logout_view(request):
    logout(request)
    redirect_url = request.META.get("HTTP_REFERER")
    if not redirect_url:
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect(redirect_url)


@csrf_exempt
def gallery_search_api(request):
    query = request.POST.get("q", None)
    if request.method == "POST":
        if not query:
            response = get_base_response()
            response["message"] = "Not enough parameters."
            response["status"] = 0
            return JsonResponse(response, status=200, safe=True)
        else:
            query = escape(query)
            authors = Author.objects.filter(Q(name__icontains=query))[:10]

            artworks = Artwork.objects.filter(Q(title__icontains=query))[:10]

            response = get_base_response()
            response["message"] = "OK"
            response["status"] = 1
            response["payload"]["data"] = render_to_string(
                "main/gallery_search_api.html",
                {"authors": authors, "artworks": artworks},
            )
            return JsonResponse(response, status=200, safe=True)
    else:
        response = get_base_response()
        response["message"] = "Wrong method. Use POST instead."
        response["status"] = 0
        return JsonResponse(response, status=200, safe=True)
