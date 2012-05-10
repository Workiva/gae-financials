from google.appengine.api import users
from google.appengine.api import oauth

# Called only if the current namespace is not set.
# This sets up the application so that each users data is
# entirely contained within a namespace.
def namespace_manager_default_namespace_for_request():
    # assumes the user is logged in.

    # check the cookies
    user = users.get_current_user()
    if user:
        return user.user_id()

    # check the oauth params
    try:
        user = oauth.get_current_user()
        if user:
            return user.user_id()
    except oauth.Error:
        pass # plain old unauthenticated access, no oauth

    return ""