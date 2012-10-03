from pyramid.view import view_config
from pyramid.response import Response
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.traversal import find_interface

from voteit.core.views.api import APIView
from voteit.core.models.interfaces import IUserTags
from voteit.core.models.interfaces import IBaseContent
from voteit.core.models.interfaces import IMeeting
from voteit.core.security import VIEW
from voteit.core.security import ROLE_VOTER

from scout.annual_meeting import ScoutMF as _


class UserTagsView(object):
    """ User tags view handles listing of users who've tagged something.
        It also performs actions to set or unset a tag
        Note that some functionality relies on the request.context attribute.
        That will be the context that the request has.
    """
    
    def __init__(self, request):
        self.api = APIView(request.context, request)
        self.request = request

    @view_config(name="_support", context=IBaseContent, permission=VIEW)
    def set_user_tag(self):
        """ View for setting or removing user tags like 'Like' or 'Support'.
            the request.POST object must contain tag and do.
            This view is usually loaded inline, but it's possible to call without js.
        """
        #FIXME: Permission for setting should perhaps be adaptive? Right now all viewers can set.
        #See https://github.com/VoteIT/voteit.core/issues/16
        #FIXME: Use normal colander Schema + CSRF?
        request = self.request
        api = self.api
        
        # Only available on proposals
        if not request.context.content_type == 'Proposal':
            raise Forbidden() 
        
        # only available if users has the vote role
        meeting = find_interface(request.context, IMeeting)
        if ROLE_VOTER not in meeting.get_groups(api.userid):
            raise HTTPForbidden()

        tag = request.POST.get('tag')
        do = int(request.POST.get('do')) #0 for remove, 1 for add

        user_tags = request.registry.getAdapter(request.context, IUserTags)

        if do:
            user_tags.add(tag, api.userid)

        if not do:
            user_tags.remove(tag, api.userid)

        if not request.is_xhr:
            return HTTPFound(location=resource_url(request.context, request))
        else:
            brains = api.get_metadata_for_query(uid = request.context.uid)
            assert len(brains) == 1
            brain = brains[0]
            return Response( api.render_single_view_component(brain, request, 'user_tags', tag, api = api) )
