# box
# Copyright 2013-2014 Dipen Patel
# See LICENSE for details.

ERRORS = {
            200 :  "success",
            201 :  "created",
            202 :  "accepted",
            204 :  "no_content",
            302 :  "redirect",
            304 :  "not_modified",
            400 :  "bad_request",
            401 :  "unauthorized",
            403 :  "forbidden",
            404 :  "not_found",
            405 :  "method_not_allowed",
            409 :  "conflict",
            412 :  "precondition_failed",
            429 :  "too_many_requests",
            500 :  "internal_server_error",
            507 :  "insufficient_storage"
          }
class BoxError(Exception):
    """Box exception"""

    def __init__(self, reason, response=None):
        self.reason = unicode(reason)
        self.response = response
        Exception.__init__(self, reason)

    def __str__(self):
        return self.reason
