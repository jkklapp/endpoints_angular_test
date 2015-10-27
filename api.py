"""This API implements the read and write services we are testing.

It uses Google Cloud Endpoints.
"""


import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote

import logging
import base64
import json
import datetime

from models import GreetingModel

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'secret'
package = 'Hello'

class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)

class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)

class JWTMessage(messages.Message):
    message = messages.StringField(1)


@endpoints.api(name='helloworld', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID],
               audiences=[WEB_CLIENT_ID])
class HelloWorldApi(remote.Service):
    """Helloworld API v1."""

    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        messages = [Greeting(message=m.message) for m in GreetingModel.all()]
        greetings = GreetingCollection(items=messages)
        return greetings

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            greeting_model = GreetingModel.get_by_id(request.id)
            return Greeting(message=greeting_model.message)
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    NEW_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            message=messages.StringField(1))

    @endpoints.method(NEW_RESOURCE, Greeting,
                      path='hellogreeting/authed', http_method='POST',
                      name='greetings.authed')
    def greeting_authed(self, request):
        # Get the HTTP Authorization header.
        auth_header = self.request_state.headers.get('authorization')
        if not auth_header:
            logging.info("No authorization header.")
        else:
            auth_token = auth_header.split(' ')[1].split('.')
            encoded_payload = json.loads(base64.b64decode(auth_token[1]))
            message = encoded_payload["message"]
            name = encoded_payload["name"]
            date = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
            new_greeting = GreetingModel(message='"%s" - %s @ %s' % (name, message, date))
        new_greeting.put()
        greeting_message = Greeting(message=new_greeting.message)
        return greeting_message



APPLICATION = endpoints.api_server([HelloWorldApi])
