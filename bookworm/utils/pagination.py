from django.core.paginator import Paginator

from bookworm.settings import PAGINATION_OBJ_PER_PAGE


def paginator(request, content, obj_per_page: int = PAGINATION_OBJ_PER_PAGE):
    paginator = Paginator(content, obj_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj
