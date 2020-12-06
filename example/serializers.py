from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Author, Book, Publish

Author1 = pydantic_model_creator(Author, exclude_readonly=True)
Author2 = pydantic_model_creator(Author, name='Author2', exclude_readonly=False)
BOOK1 = pydantic_model_creator(Book, exclude_readonly=True,allow_cycles=True, name='BOOK1')
BOOK2 = pydantic_model_creator(Book, exclude_readonly=False,allow_cycles=True, name='BOOK2')
