'''Types for User'''
from typing import TypedDict


class UserJSONType(TypedDict):
    '''Refers to the JSON returned for a user'''
    id: str
    email: str
    username: str
    role: str
    first_name: str
    last_name: str
