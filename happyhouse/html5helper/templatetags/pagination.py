# coding=utf-8

from django import template


register = template.Library()


@register.inclusion_tag("html5helper/tags/pagination.html", name="pagination")
def do_pagination(pager, prefix):
    """
        1: 1 ~ 10
        2: 1 ~ 10
        3: 1 ~ 10
        4: 1 ~ 10
        5: 1 ~ 10
        6: 6 ~ 15
        7: 6 ~ 15
        8: 6 ~ 15
        9: 6 ~ 15
        10: 6 ~ 15
        11: 11 ~ 20
    Args:
        pager:
        prefix:

    Returns:

    """
    if not pager:
        return {"pager": None}

    if prefix and prefix[-1] == "/":
        prefix = prefix[:len(prefix) - 1]

    cur_page = pager.number
    if cur_page % 5:
        start = (cur_page / 5) * 5 + 1
    else:
        start = (cur_page / 5 - 1) * 5 + 1
    end = start + 9

    if end >= pager.paginator.num_pages:
        end = pager.paginator.num_pages

    pages = range(start, end + 1)

    if cur_page > 1:
        first_pages = True
    else:
        first_pages = False

    if cur_page < pager.paginator.num_pages:
        last_pages = True
    else:
        last_pages = False

    return {"pager": pager, "prefix": prefix, "pages": pages, "last_pages": last_pages, "first_pages": first_pages}
