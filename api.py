"""This API implements the read and write services we are testing.

It uses Google Cloud Endpoints.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from models import GreetingModel

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'

package = 'Hello'


class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


@endpoints.api(name='helloworld', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID
                                   ],
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
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None
                 else 'Anonymous')
        new_greeting = GreetingModel(message='hello %s, you wrote "%s"!' % (email, request.message))
        new_greeting.put()
        greeting_message = Greeting(message=new_greeting.message)
        return greeting_message


APPLICATION = endpoints.api_server([HelloWorldApi])
