from datetime import datetime


def get_current_date(request):
    """Return the current date."""
    return {'today': datetime.now()}
