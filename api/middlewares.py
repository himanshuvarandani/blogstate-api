# All falcon middlewares #

from api.models import db
import falcon
import inspect
import os


ENV_FILENAME = '.env'

# Switching to reading static file, since loading environment
# variables causes nuisance in production server.

this_module = inspect.getfile(inspect.currentframe())
this_dir = os.path.dirname(this_module)
envfile_path = os.path.join(this_dir, ENV_FILENAME)
with open(envfile_path) as fp:
    KEY = fp.readline().rstrip("\n")


class PeeweeConnectionMiddleware(object):
    # :- Middleware for peewee reconnection -: #

    def process_request(self, req, resp):
        if db.is_closed():
            db.connect()


class SourceVerifierMiddleware(object):
    """
    Check if the agent calling the API is a trusted source,
    by checking the authorization token in request headers.
    """
    def process_request(self, req, resp):
        if not self._load_token_and_validate(req):
            raise falcon.HTTPUnauthorized('No authorization token found'
                                          'in request.')

    def _load_token_and_validate(self, req):
        if req.get_header('Authorization') == KEY:
            return True
        return False
