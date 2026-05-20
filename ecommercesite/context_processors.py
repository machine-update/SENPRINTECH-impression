from urllib.parse import quote

from django.conf import settings


def whatsapp(request):
    message = settings.WHATSAPP_GENERAL_MESSAGE
    return {
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
        "WHATSAPP_DISPLAY_NUMBER": settings.WHATSAPP_DISPLAY_NUMBER,
        "WHATSAPP_GENERAL_MESSAGE": message,
        "WHATSAPP_GENERAL_URL": f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(message)}",
    }
