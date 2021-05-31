from .calendar import get_date_today


def get_current_date(request):
    """Return the current date."""
    return {'today': get_date_today()}
