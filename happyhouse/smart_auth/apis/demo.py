#encoding=utf-8
from html5helper.decorator import render_json
from smart_auth.utils import check_permission_for_api


@render_json
@check_permission_for_api
def demo_api(request):
    return {"is_ok":True}
demo_api.__permission_name__ = u"测试用的API"

