from pydantic import TypeAdapter, BaseModel, Field
from typing import Literal
import json
from typing import Annotated, Union
from enum import Enum
from pydantic import BaseModel
from pydantic import TypeAdapter, BaseModel, Field
from typing import Annotated, Union


class SpecialType(str, Enum):
    FOOO = "fooo"
    BRANCHA = "branchA"
    BRANCHB = "branchB"


foobar = Annotated[Union["BranchA", "BranchB", "Leaf"], Field(discriminator="type")]


class Leaf(BaseModel):
    type: Literal[SpecialType.FOOO] = SpecialType.FOOO
    leaf: str


class BranchA(BaseModel):
    type: Literal["branchA"] = "branchA"
    branches: list[foobar]


class BranchB(BaseModel):
    type: Literal["branchB"] = "branchB"
    branches: list[foobar]


FooBar = TypeAdapter(foobar)
