import colander
from deform import Form
from deform.exception import ValidationFailure
from betahaus.viewcomponent import view_action
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound

from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_request
from voteit.core.models.schemas import button_cancel
from voteit.core.security import ROLE_DISCUSS
from voteit.core.models.interfaces import IMeeting

from scout.annual_meeting import ScoutMF as _


@view_action('request_meeting_access', 'view_and_discuss_permissions',
             interface = IMeeting,
             title = _(u"meeting_access_view_and_discuss_label",
                       default = u"All users will be given view and discuss permissions INSTANTLY if they request it."),)
def meeting_access_view_and_discuss(context, request, va, **kw):
    if context.get_field_value('access_policy') != 'view_and_discuss_permissions':
        raise Exception("ViewAction for request meeting access view_and_discuss_permissions was called, but that access policy wasn't set for this meeting.")
    api = kw['api']
    if not api.userid:
        raise Exception("Can't find userid")
    schema = colander.Schema()
    add_csrf_token(context, request, schema)
    form = Form(schema, buttons=(button_request, button_cancel,))
    response = {'api': api}
    post = request.POST
    if 'request' in post:
        controls = post.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            response['form'] = e.render()
            return response
        context.add_groups(api.userid, [ROLE_DISCUSS, ], event = True)
        api.flash_messages.add(_(u"Access granted!"))
        url = resource_url(context, request)
        return HTTPFound(location=url)

    msg = _(u"meeting_access_view_and_discuss_description",
            default = u"This meeting allows anyone to request access to it. You only need to click below to get view and discuss permissions instantly.")
    api.flash_messages.add(msg)
    #No action - Render form
    return form.render()