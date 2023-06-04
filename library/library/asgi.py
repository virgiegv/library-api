"""
ASGI config for library project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from api.schema import schema
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

application = get_asgi_application() #this doesnt get mounted, until we're doing testing

fastapp = FastAPI()
fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

fastapp.mount(
    '/graphql', GraphQLApp(schema, on_get=make_graphiql_handler())
)

