from pydantic import BaseModel, Field
from typing import Optional, Literal, Union

class Identified(BaseModel):
    id: str = Field(alias='@id')

class BranchRequest(BaseModel):
    name: str
    head: Identified

class Branch(BaseModel):
    id: str = Field(alias='@id')
    name: str
    created: str
    head: Identified
    owningProject: Identified
    referencedCommit: Identified
    type: Literal['Branch'] = Field(default='Branch', alias='@type')

class Project(BaseModel):
    id: str = Field(alias='@id')
    name: str
    created: str
    description: str
    defaultBranch: Identified
    type: Literal['Project'] = Field(default='Project', alias='@type')

class ProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
    defaultBranch: Optional[Identified] = None


class Tag(BaseModel):
    id: str = Field(alias='@id')
    name: str
    created: str
    referencedCommit: Identified
    owningProject: Identified
    taggedCommit: Identified
    type: Literal["Tag"] = Field(default='Tag', alias='@type')

class TagRequest(BaseModel):
    name: str
    taggedCommit: Identified

class Commit(BaseModel):
    id: str = Field(alias='@id')
    created: str
    owningProject: Identified
    description: str
    previousCommit: Optional[Identified] = None
    type: Literal['Commit'] = Field(default='Commit', alias='@type')

class PrimitiveConstraint(BaseModel):
    value: Union[str, int, float, bool, Identified]
    operator: Literal['=', '>', '<']
    inverse: bool
    property: str
    
class CompositeConstraint(BaseModel):
    constraint: list[PrimitiveConstraint]
    operator: Literal['and', 'or']

class Query(BaseModel):
    id: str = Field(alias='@id')
    owningProject: Identified
    select: list[str]
    where: Union[CompositeConstraint, PrimitiveConstraint]
    type: Literal['Query'] = Field(default='Query', alias='@type')

class QueryRequest(BaseModel):
    select: list[str]
    where: Union[CompositeConstraint, PrimitiveConstraint]
