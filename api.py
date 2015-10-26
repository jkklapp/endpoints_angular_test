"""This API implements the read and write services we are testing.

It uses Google Cloud Endpoints.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


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


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


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
        return STORED_GREETINGS

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            return STORED_GREETINGS.items[request.id]
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
        new_greeting = Greeting(message='hello %s, you wrote "%s"!' % (email, request.message))
        STORED_GREETINGS.items.append(new_greeting)
        return new_greeting


APPLICATION = endpoints.api_server([HelloWorldApi])
