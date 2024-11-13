from datetime import datetime


def year(request):
    """Переменная с текущим годом."""
    year_now = datetime.now().year
    return {
        "year": year_now
    }
