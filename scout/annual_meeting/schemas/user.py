import colander
from betahaus.pyracont.decorators import schema_factory

from voteit.core import VoteITMF
from voteit.core.validators import html_string_validator 
from voteit.core.schemas import user

from scout.annual_meeting import ScoutMF as _


def scout_group_node():
    return colander.SchemaNode(colander.String(),
                               title=_(u"Scout group"),
                               validator=html_string_validator,)


@schema_factory('AddUserSchema', title = VoteITMF(u"Add user"), description = VoteITMF(u"Use this form to add a user"))
class AddUserSchema(user.AddUserSchema):
    """ Used for regular add command. """
    scout_group = scout_group_node()


@schema_factory('RegisterUserSchema', title = VoteITMF(u"Registration"))
class RegisterUserSchema(user.RegisterUserSchema):
    """ Used for registration. """
    scout_group = scout_group_node()


@schema_factory('EditUserSchema', title = VoteITMF(u"Edit user"), description = VoteITMF(u"Use this form to edit a user"))
class EditUserSchema(user.EditUserSchema):
    """ Regular edit. """
    scout_group = scout_group_node()
