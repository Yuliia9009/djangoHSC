import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth import logout
from utils.email_notifications import send_subscription_confirmation_email
from django.contrib import messages

from .forms import UserSearchForm
from .services import check_available_plates
from .models import TSC, UserSearch, Region, VehicleType, SearchSubscription, AvailableResult

@login_required
def create_search(request):
    form = UserSearchForm()

    if request.method == 'POST':
        if 'clear_search_history' in request.POST:
            UserSearch.objects.filter(user=request.user).delete()
            return redirect('create_search')

        form = UserSearchForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.user = request.user
            search.save()
            form.save_m2m()

            digits = form.cleaned_data["digits"]
            region_code = form.cleaned_data["region"].code
            tsc = form.cleaned_data.get("selected_tsc")
            tsc_code = tsc.code if tsc else None

            vehicle_type_obj = form.cleaned_data["vehicle_type"]
            vehicle_type_code = vehicle_type_obj.code

            results = check_available_plates(digits, region_code, tsc_code, vehicle_type_code)

            return render(request, 'autonumbers/results.html', {
                'results': results,
                'raw_results_json': json.dumps(results, ensure_ascii=False),
                'digits': digits,
                'region': form.cleaned_data["region"].id,
                'tsc': tsc.id if tsc else '',
                'vehicle_type': vehicle_type_obj.id
            })

    return render(request, 'autonumbers/create_search.html', {'form': form})

@login_required
def my_searches(request):
    searches = UserSearch.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'autonumbers/my_searches.html', {'searches': searches})


def load_tscs(request):
    region_id = request.GET.get('region')
    tscs = TSC.objects.filter(region_id=region_id).order_by('name')
    return JsonResponse(list(tscs.values('id', 'name')), safe=False)


@login_required
@require_POST
def subscribe_search(request):
    region_id = request.POST.get("region")
    tsc_id = request.POST.get("tsc") or None
    vehicle_type_id = request.POST.get("vehicle_type")
    digits = request.POST.get("digits")

    region = Region.objects.get(pk=region_id)
    vehicle_type = VehicleType.objects.get(pk=vehicle_type_id)
    tsc = TSC.objects.get(pk=tsc_id) if tsc_id else None

    exists = SearchSubscription.objects.filter(
        user=request.user,
        region=region,
        selected_tsc=tsc,
        vehicle_type=vehicle_type,
        digits=digits
    ).exists()

    if exists:
        messages.warning(request, "⚠️ Ви вже підписані на цей запит.")
        return redirect('profile_page')

    subscription = SearchSubscription.objects.create(
        user=request.user,
        region=region,
        selected_tsc=tsc,
        vehicle_type=vehicle_type,
        digits=digits
    )

    send_subscription_confirmation_email(request.user.email, subscription)
    messages.success(request, "✅ Ви успішно підписалися на моніторинг.")
    return redirect('profile_page')


@login_required
def cancel_subscription(request, pk):
    subscription = get_object_or_404(SearchSubscription, pk=pk, user=request.user)
    if request.method == "POST":
        subscription.delete()
    return redirect("profile_page")


def search_success(request):
    return render(request, 'autonumbers/success.html')

def home_page(request):
    return render(request, 'autonumbers/home.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    found_total = AvailableResult.objects.count()
    return render(request, 'autonumbers/home.html', {
        'found_total': found_total
    })