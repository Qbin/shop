#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from pp.models import Problem

register = template.Library()


@register.filter("show_problem_status")
def do_show_problem_status(id):
    for tup in Problem.STATUS_CHOICES:
        if id == tup[0]:
            return tup[1]
    return u"错误类型"

@register.filter("show_category")
def do_show_category(id):
    if not id:
        return ""
    elif id not in xrange(1, 4):
        return ""

    category = [
        "分类",
        "回归",
        "聚类",
    ]
    return category[id - 1]


@register.filter("show_status")
def do_show_status(id):
    if id == 1:
        color = "009900"
        name = "成功"
    elif id == 2:
        color = "000099"
        name = "运算中"
    elif id == 3:
        color = "990000"
        name = "失败"
    elif id == 4:
        color = "999900"
        name = "新建"
    elif id == 5:
        color = "990000"
        name = "运行超时"
    elif id == 6:
        color = "990000"
        name = "内存溢出"
    elif id == 7:
        color = "990000"
        name = "编译失败"
    else:
        color = "999999"
        name = "无状态"

    html = '<span style="color: #%s">%s</span>' % (color, name)

    return html


@register.filter("show_kpi")
def do_show_kpi(kpi, bit):
    """

    Args:
        kpi: 需要格式化的KPI的值
        bit: 保留的小数点的位数

    Returns: 格式化之后的kpi值

    """
    if kpi:
        fmt = '%%.%df' % bit
        kpi = fmt % kpi
    else:
        kpi = "- -"

    return kpi


@register.filter("show_msec")
def do_show_msec(msec, bit):
    """

    Args:
        msec: 需要格式化的毫秒的值
        bit: 保留的小数点的位数

    Returns: 格式化之后的毫秒值

    """
    if msec:
        msec = str(round(msec, bit)) + "毫秒"
    else:
        msec = "- -"

    return msec
