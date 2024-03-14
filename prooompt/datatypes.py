from enum import Enum
from pydantic import BaseModel
from pydantic import TypeAdapter, BaseModel, Field
from typing import Annotated, Union, Literal


# enums
class MessageRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class TemplateItemType(str, Enum):
    MESSAGE = "message"
    TEXT = "text"
    EVAL = "eval"
    LOOP = "loop"


# openai message
class Message(BaseModel):
    role: MessageRole
    content: str


# template items
TemplateItemUnion = Annotated[
    Union["TemplateMessage", "TemplateText", "TemplateEval", "TemplateLoop"],
    Field(discriminator="type"),
]


# message template
class TemplateMessage(BaseModel):
    type: Literal[TemplateItemType.MESSAGE] = TemplateItemType.MESSAGE
    role: MessageRole
    template: list[TemplateItemUnion]


# text template
class TemplateText(BaseModel):
    type: Literal[TemplateItemType.TEXT] = TemplateItemType.TEXT
    content: str


# eval template
class TemplateEval(BaseModel):
    type: Literal[TemplateItemType.EVAL] = TemplateItemType.EVAL
    value: str


# loop template
class TemplateLoop(BaseModel):
    type: Literal[TemplateItemType.LOOP] = TemplateItemType.LOOP
    iterator: str
    iterable: str
    template: list[TemplateItemUnion]


# overall template
class Template(BaseModel):
    items: list[TemplateItemUnion]


# general type adapter for template items
TemplateItem = TypeAdapter(TemplateItemUnion)
