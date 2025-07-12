from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now

from .models import SearchSubscription
from .services import check_available_plates

@staff_member_required
def admin_subscriptions_view(request):
    subscriptions = SearchSubscription.objects.all().order_by('-created_at')

    if request.method == "POST":
        if "run_all" in request.POST:
            for sub in subscriptions:
                _run_subscription_check(sub)
            return redirect("admin_subscriptions")

        elif "run_one" in request.POST:
            sub_id = request.POST.get("sub_id")
            sub = get_object_or_404(SearchSubscription, id=sub_id)
            _run_subscription_check(sub)
            return redirect("admin_subscriptions")

        elif "delete_one" in request.POST:
            sub_id = request.POST.get("sub_id")
            SearchSubscription.objects.filter(id=sub_id).delete()
            return redirect("admin_subscriptions")

    return render(request, "autonumbers/admin_subscriptions.html", {
        "subscriptions": subscriptions
    })


def _run_subscription_check(sub):
    results = check_available_plates(
        digits=sub.digits,
        region_code=sub.region.code,
        tsc_code=sub.selected_tsc.code if sub.selected_tsc else None,
        vehicle_type=sub.vehicle_type.code
    )
    sub.last_checked = now()
    sub.save()
