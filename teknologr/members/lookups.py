from ajax_select import register, LookupChannel
from members.models import *
from django.utils.html import escape
from api.utils import findMembers


@register('member')
class MemberLookup(LookupChannel):

    model = Member

    def get_query(self, q, request):

        members = findMembers(q)
        return members

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj._get_full_name()

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return obj._get_full_name()

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return obj._get_full_name()
