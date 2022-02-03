import datetime
import re
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

from .models import Painting
from accounts.models import CustomUser


def get_base_response():
    return {"message": None, "status": 0, "payload": {}}


def home(request):
    return render(request, "main/coming_soon.html")


def projects(request):
    return render(request, "main/dev.html")


def handler404(request, exception):
    return render(request, "main/404.html", status=404)


def handler500(request):
    return render(request, "main/500.html", status=500)


def handler401(request):
    return render(request, "main/401.html", status=401)


def handler400(request, exception):
    return render(request, "main/400.html", status=400)


def handler403(request, exception):
    return render(request, "main/403.html", status=403)


def gallery(request):
    try:
        price__max, price__min = Painting.objects.aggregate(
            Max("price"), Min("price")
        ).values()
        year__max, year__min = (
            i.year for i in Painting.objects.aggregate(Max("date"), Min("date")).values()
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

    sa = request.GET.get("sa", False)
    nft = request.GET.get("nft", False)
    av = request.GET.get("av", False)

    if pid and pid.isdigit():
        paintings = Painting.objects.filter(id=pid)

    elif aid and aid.isdigit():
        paintings = Painting.objects.filter(author__id=aid)

    elif f:
        _sa = Q(is_offline_available=bool(sa)) if sa else ~Q(pk__in=[])
        _nft = Q(is_nft=bool(nft)) if nft else ~Q(pk__in=[])
        _av = Q(author__is_painter=bool(av)) if av else ~Q(pk__in=[])

        if ps.isdigit() and pe.isdigit() and ys.isdigit() and ye.isdigit():
            paintings = Painting.objects.filter(
                Q(price__range=[int(ps), int(pe)]) &
                Q(
                    date__range=[
                        datetime.date(int(ys), 1, 1),
                        datetime.date(int(ye), 12, 31),
                    ]
                ) &
                _sa &
                _nft &
                _av
            )

    else:
        paintings = Painting.objects.all()

    return render(
        request,
        "main/gallery.html",
        {
            "paintings": paintings,
            "price__max": price__max,
            "price__min": price__min,
            "price__min__value": price__min__value,
            "price__max__value": price__max__value,
            "year__max": year__max,
            "year__min": year__min,
            "year__min__value": year__min__value,
            "year__max__value": year__max__value,
            "sa": sa,
            "nft": nft,
            "av": av,
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
            authors = CustomUser.objects.annotate(
                full_name=Concat("first_name", V(" "), "last_name")
            ).filter(Q(full_name__icontains=query) & Q(is_painter=True))[:10]

            paintings = Painting.objects.annotate(
                full_name=Concat("author__first_name", V(" "), "author__last_name")
            ).filter(
                (Q(name__icontains=query) | Q(full_name__icontains=query))
                & Q(author__is_painter=True)
            )[
                :10
            ]

            response = get_base_response()
            response["message"] = "OK"
            response["status"] = 1
            response["payload"]["data"] = render_to_string(
                "main/gallery_search_api.html",
                {"authors": authors, "paintings": paintings},
            )
            return JsonResponse(response, status=200, safe=True)
    else:
        response = get_base_response()
        response["message"] = "Wrong method. Use POST instead."
        response["status"] = 0
        return JsonResponse(response, status=200, safe=True)
