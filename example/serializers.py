from tortoise.contrib.pydantic import pydantic_model_creator

from .models import *

book = pydantic_model_creator(Book)
Author1 = pydantic_model_creator(Author)
Author2 = pydantic_model_creator(Author, name='Author2', exclude_readonly=False)
BOOK1 = pydantic_model_creator(Book, exclude_readonly=True, allow_cycles=True, name='BOOK1')
BOOK2 = pydantic_model_creator(Book, name='BOOK2')
Event_Pydantic = pydantic_model_creator(Event)
Tournament_Pydantic = pydantic_model_creator(Tournament)
Team_Pydantic = pydantic_model_creator(Team)
