from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from pyramid.traversal import find_resource
from pyramid.traversal import find_interface

from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IUserTags
from voteit.core.security import ROLE_VOTER

from scout.annual_meeting import ScoutMF as _


@view_action('user_tags', 'support')
def user_tag_i_support(brain, request, va, **kw):
    """ Special view action for user tag 'support'.
        It requires catalog metadata + expects a brain
        as context, rather than a full object.
    """
    api = kw['api']
    
    obj = find_resource(api.root, brain['path'])
    # Only available on proposals
    if not obj.content_type == 'Proposal':
        return "" 
    
    # only available if users has the vote role
    meeting = find_interface(obj, IMeeting)
    if ROLE_VOTER not in meeting.get_groups(api.userid):
        return ""
    
    show_form = kw.get('show_form', True) 
    user_tags = request.registry.getAdapter(obj, IUserTags)
    userids = user_tags.userids_for_tag('support')
    #Note: It's not possible to have nested translation strings. So we do the translation here in advance.
    display_name =  api.translate(_(u"Support"))
    expl_display_name = _(u"Support this")
    brain_url = "%s%s" % (request.application_url, brain['path'])
    
    response = dict(
        context_id = brain['uid'],
        toggle_url = "%s/_support" % brain_url,
        tag = 'support',
        display_name = display_name,
        get_userinfo_url = api.get_userinfo_url,
        expl_display_name = expl_display_name,
    )
    
    if api.userid and api.userid in userids:
        #Current user likes the current context
        response['button_label'] = _(u"Remove ${display_name}",
                                     mapping={'display_name': display_name})
        response['selected'] = True
        response['do'] = "0"
        userids = list(userids)
        userids.remove(api.userid)
    else:
        #Current user hasn't selected the current context
        response['button_label'] = display_name
        response['selected'] = False
        response['do'] = "1"

    response['userids'] = userids
    response['has_entries'] = bool(response['selected'] or userids)
    response['tagging_users_url'] =" %s/_tagging_users?tag=%s&display_name=%s&expl_display_name=%s" % (brain_url, 'i_support', display_name, expl_display_name)
    response['show_form'] = show_form

    return render('voteit.core.views:templates/snippets/user_tag.pt', response, request = request)
