# admin.py
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.timezone import now
from .models import Region, UserSearch, AvailableResult, SearchSubscription
from .services import check_available_plates
from utils.email_notifications import send_search_results_email

import csv
from django.http import HttpResponse


@admin.register(SearchSubscription)
class SearchSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user_link', 'digits', 'region', 'selected_tsc',
        'vehicle_type', 'created_at', 'last_checked', 'found_results_count'
    )
    list_filter = ('region', 'vehicle_type')
    search_fields = ('digits', 'user__username')
    actions = ['run_now', 'export_as_csv']

    def user_link(self, obj):
        return format_html('<a href="/admin/auth/user/{}/change/">{}</a>', obj.user.id, obj.user.username)

    user_link.short_description = "Користувач"

    def found_results_count(self, obj):
        return obj.available_results.count()

    found_results_count.short_description = "Знайдено номерів"

    @admin.action(description="🔍 Запустити пошук зараз")
    def run_now(self, request, queryset):
        total = 0
        for sub in queryset:
            results = check_available_plates(
                digits=sub.digits,
                region_code=sub.region.code,
                tsc_code=sub.selected_tsc.code if sub.selected_tsc else None,
                vehicle_type=sub.vehicle_type.code
            )

            if results:
                for plate_info in results:

                    print("plate_info =", plate_info)

                    plate_value = plate_info.get('plate') or plate_info.get('number')
                    if not plate_value:
                        print("⚠️ Немає ні 'plate', ні 'number':", plate_info)
                        continue

                    AvailableResult.objects.create(
                        subscription=sub,
                        plate=plate_value,
                        price=plate_info.get('price'),
                        location=plate_info.get('location', '')
                    )

                send_search_results_email(sub.user.email, results, sub)
                total += len(results)

            sub.last_checked = now()
            sub.save()

        self.message_user(
            request,
            f"Пошук запущено для {queryset.count()} підписок. Всього знайдено {total} номерів.",
            messages.SUCCESS
        )

    @admin.action(description="⬇️ Експорт у CSV")
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=subscriptions.csv'
        writer = csv.writer(response)
        writer.writerow(['User', 'Digits', 'Region', 'TSC', 'Vehicle Type', 'Created'])
        for sub in queryset:
            writer.writerow([
                sub.user.username,
                sub.digits,
                sub.region.name,
                sub.selected_tsc.name if sub.selected_tsc else '',
                sub.vehicle_type.name,
                sub.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        return response


@admin.register(UserSearch)
class UserSearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'digits', 'region', 'selected_tsc', 'vehicle_type', 'created_at')
    list_filter = ('region', 'vehicle_type')
    search_fields = ('digits', 'user__username')


@admin.register(AvailableResult)
class AvailableResultAdmin(admin.ModelAdmin):
    list_display = ('plate', 'price', 'location', 'subscription', 'found_at')
    list_filter = ('location',)
    search_fields = ('plate', 'subscription__user__username')
    date_hierarchy = 'found_at'


admin.site.register(Region)