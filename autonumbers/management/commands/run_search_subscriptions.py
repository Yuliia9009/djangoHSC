from django.core.management.base import BaseCommand
from django.utils.timezone import now

from autonumbers.models import SearchSubscription
from autonumbers.services import check_available_plates
from utils.email_notifications import send_search_results_email

class Command(BaseCommand):
    help = "Run search for active subscriptions"

    def handle(self, *args, **kwargs):
        for sub in SearchSubscription.objects.all():
            results = check_available_plates(
                digits=sub.digits,
                region_code=sub.region.code,
                tsc_code=sub.selected_tsc.code if sub.selected_tsc else None,
                vehicle_type=sub.vehicle_type.code,
            )

            if results:
                send_search_results_email(sub.user.email, results, sub)

                sub.last_checked = now()
                sub.save()