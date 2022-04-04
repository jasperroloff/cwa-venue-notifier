from django.conf import settings


def global_vars(request):
    return {
        'global_imprint_url': settings.GLOBAL_IMPRINT_URL,
        'global_privacy_url': settings.GLOBAL_PRIVACY_URL,
    }
