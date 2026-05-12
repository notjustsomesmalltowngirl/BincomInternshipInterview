from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import PollingUnit, AnnouncedPuResults, Lga


def home(request):
    polling_units = PollingUnit.objects.all()

    if request.method == "POST":
        selected_id = request.POST.get("polling_unit")
        return redirect("polling_unit_results", uniqueid=selected_id)

    return render(request, "home.html", {
        "polling_units": polling_units
    })

def polling_unit_results(request, uniqueid):
    polling_unit = get_object_or_404(PollingUnit, uniqueid=uniqueid)

    results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=str(uniqueid))

    context = {
        "polling_unit": polling_unit,
        "results": results
    }

    return render(request, "pu_result.html", context)

def lga_results(request):
    lgas = Lga.objects.all()
    results = None
    selected_lga = None

    if request.method == "POST":
        lga_id = request.POST.get("lga_id")
        selected_lga = Lga.objects.get(uniqueid=lga_id)

        polling_units = PollingUnit.objects.filter(lga_id=lga_id)

        pu_ids = [pu.uniqueid for pu in polling_units]

        results = AnnouncedPuResults.objects.filter(
            polling_unit_uniqueid__in=[str(i) for i in pu_ids]
        ).values("party_abbreviation").annotate(
            total_score=Sum("party_score")
        )

    return render(request, "lga_results.html", {
        "lgas": lgas,
        "results": results,
        "selected_lga": selected_lga
    })


def create_results(request):
    polling_units = PollingUnit.objects.all()

    if request.method == "POST":
        pu_id = request.POST.get("polling_unit")

        parties = ["PDP", "APC", "LP", "NNPP"]

        for party in parties:
            score = request.POST.get(party)

            AnnouncedPuResults.objects.create(
                polling_unit_uniqueid=str(pu_id),
                party_abbreviation=party,
                party_score=int(score),
                entered_by_user="admin",
                user_ip_address="127.0.0.1"
            )

        return redirect("home")

    return render(request, "create_results.html", {
        "polling_units": polling_units
    })