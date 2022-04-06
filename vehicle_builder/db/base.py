import re

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', cls.__name__).lower()

    def __str__(self):
        print_string = f"{self.__class__.__name__}: "
        if hasattr(self, "name"):
            print_string += self.name
        else:
            print_string += f"#{self.id}"
        return print_string
