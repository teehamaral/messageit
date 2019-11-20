import requests

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from temba.contacts.models import WHATSAPP_SCHEME

from ...models import ChannelType, Channel
from .views import ClaimView


class ChatAPIType(ChannelType):
    """
    A Chat API instance channel
    """

    code = "CA"
    category = ChannelType.Category.SOCIAL_MEDIA

    courier_url = r"^ca/(?P<uuid>[a-z0-9\-]+)/receive$"

    name = "Chat API"
    icon = "icon-whatsapp"
    show_config_page = False

    claim_blurb = _(
        """Add a <a href="https://chat-api.com/en/">Chat API</a> instance to send and receive messages to WhatsApp
    users. Your users will need an Android or iOS device and a WhatsApp account to send and receive
    messages."""
    )
    claim_view = ClaimView

    schemes = [WHATSAPP_SCHEME]
    max_length = 1600
    attachment_support = True

    def activate(self, channel):
        config = channel.config
        auth_token = config.get(Channel.CONFIG_AUTH_TOKEN)
        send_url = config.get(Channel.CONFIG_SEND_URL)

        webhook_url = f"https://{channel.callback_domain}{reverse('courier.ca', args=[channel.uuid])}"

        webhook_payload = {"set": True, "webhookUrl": webhook_url}
        ack_notification_payload = {"ackNotificationsOn": 1}

        set_webhook_url = f"{send_url}/webhook?token={auth_token}"
        set_ack_url = f"{send_url}/settings/ackNotificationsOn?token={auth_token}"

        # Setting up the webhook
        requests.post(set_webhook_url, data=webhook_payload)

        # Setting up the Ack notification
        requests.post(set_ack_url, data=ack_notification_payload)
