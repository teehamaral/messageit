import requests
from smartmin.views import SmartFormView

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ...models import Channel
from ...views import ClaimViewMixin


class ClaimView(ClaimViewMixin, SmartFormView):
    class Form(ClaimViewMixin.Form):
        channel_name = forms.CharField(label=_("Channel Name"), help_text=_("The name of the channel"), required=True)
        whatsapp_phone_number = forms.CharField(
            label=_("WhatsApp Phone Number"),
            help_text=_("Your WhatsApp Phone Number. E.g. 558299009900"),
            required=True,
        )
        send_url = forms.CharField(
            label=_("URL"), help_text=_("The Chat API URL, you can find it on the Chat API dashboard"), required=True
        )
        auth_token = forms.CharField(
            label=_("Authentication Token"),
            help_text=_("The Authentication token for this instance, you can find it on the Chat API dashboard"),
            required=True,
        )

        def clean(self):
            org = self.request.user.get_org()
            auth_token = self.cleaned_data["auth_token"]
            send_url = self.cleaned_data["send_url"]

            # does a bot already exist on this account with that auth token
            for channel in Channel.objects.filter(org=org, is_active=True, channel_type=self.channel_type.code):
                if channel.config["auth_token"] == auth_token:
                    raise ValidationError(_("A Chat API channel with this token already exists on your account."))

            # Removing the / from the end if it exists
            if send_url.endswith("/"):
                send_url = send_url[: len(send_url) - 1]

            full_api_url = f"{send_url}/status?token={auth_token}"

            response = requests.get(full_api_url)
            if response.status_code != 200:
                raise ValidationError(_("Please check your credentials."))

            return self.cleaned_data

    form_class = Form

    def form_valid(self, form):
        org = self.request.user.get_org()
        auth_token = self.form.cleaned_data["auth_token"]
        send_url = self.form.cleaned_data["send_url"]
        channel_name = self.form.cleaned_data["channel_name"]
        whatsapp_phone_number = self.form.cleaned_data["whatsapp_phone_number"]

        channel_config = {Channel.CONFIG_AUTH_TOKEN: auth_token, Channel.CONFIG_SEND_URL: send_url}

        self.object = Channel.create(
            org,
            self.request.user,
            None,
            self.channel_type,
            name=channel_name,
            address=whatsapp_phone_number,
            config=channel_config,
        )

        return super().form_valid(form)
