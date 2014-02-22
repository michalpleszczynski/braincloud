# coding: utf-8
from core.base_api import BaseResource

from .index import search_in_title_and_tags


class TextThoughtAjaxResource(BaseResource):

    class Meta:
        resource_name = 'livesearch'

    def post_list(self, request, **kwargs):
        phrase = request.POST.get('q')
        if phrase:
            thoughts = search_in_title_and_tags(1, phrase)
            return self.create_response(request, thoughts)
