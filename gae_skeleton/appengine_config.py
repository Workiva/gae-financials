from google.appengine.api import users

# Called only if the current namespace is not set.
# This sets up the application so that each users data is
# entirely contained within a namespace.
def namespace_manager_default_namespace_for_request():
    # assumes the user is logged in.
    return users.get_current_user().user_id()