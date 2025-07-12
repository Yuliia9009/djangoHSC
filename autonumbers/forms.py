from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import UserSearch, Region, TSC, VehicleType


class LoginForm(forms.Form):
    username = forms.CharField(label="Логін")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=15, label="Номер телефону (067...)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False, label="Номер телефону (067...)")

    class Meta:
        model = User
        fields = ['email']


class UserSearchForm(forms.ModelForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        label="Оберіть область",
        empty_label=None
    )

    selected_tsc = forms.ModelChoiceField(
        queryset=TSC.objects.none(),
        required=False,
        label="ТСЦ (необов’язково)"
    )

    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.all(),
        label="Оберіть тип транспорту",
        empty_label=None
    )

    digits = forms.CharField(
        required=False,
        max_length=4,
        label="Бажана комбінація (4 цифри)",
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message="Введіть рівно 4 цифри або залиште поле порожнім",
                code='invalid_digits'
            )
        ]
    )

    class Meta:
        model = UserSearch
        fields = ['region', 'selected_tsc', 'vehicle_type', 'digits']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.data.get('region') and not self.instance.pk:
            first_region = Region.objects.first()
            if first_region:
                self.fields['region'].initial = first_region.pk
                self.fields['selected_tsc'].queryset = TSC.objects.filter(region=first_region)

        if not self.data.get('vehicle_type') and not self.instance.pk:
            first_type = VehicleType.objects.first()
            if first_type:
                self.fields['vehicle_type'].initial = first_type.pk

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['selected_tsc'].queryset = TSC.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['selected_tsc'].queryset = self.instance.region.tscs.all()