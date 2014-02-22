# coding: utf-8
from tastypie.resources import (ModelDeclarativeMetaclass, Resource,
                                ModelResource)
from tastypie.paginator import Paginator


class NoMetaPaginator(Paginator):
    """
    Paginator with no meta.
    """
    def page(self):
        res = super(NoMetaPaginator, self).page()
        del res['meta']
        return res


class BaseResource(Resource):
    pass
