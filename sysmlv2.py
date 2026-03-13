from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, Union

class Identified(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='@id')

class BranchRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    head: Identified

class Branch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='@id')
    name: str
    created: str
    head: Identified
    owningProject: Identified
    referencedCommit: Identified
    type: Literal['Branch'] = Field(default='Branch', alias='@type')

class Project(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='@id')
    name: str
    created: str
    description: str
    defaultBranch: Identified
    type: Literal['Project'] = Field(default='Project', alias='@type')

class ProjectRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    description: Optional[str] = None
    defaultBranch: Optional[Identified] = None


class Tag(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='@id')
    name: str
    created: str
    referencedCommit: Identified
    owningProject: Identified
    taggedCommit: Identified
    type: Literal["Tag"] = Field(default='Tag', alias='@type')

class TagRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    taggedCommit: Identified

class Commit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='@id')
    created: str
    owningProject: Identified
    description: str
    previousCommit: Optional[Identified] = None
    type: Literal['Commit'] = Field(default='Commit', alias='@type')

class Payload(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')

    id: str = Field(alias='@id')
    type: str = Field(alias='@type')

class DataVersionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    payload: Optional[Payload]
    identity: Optional[Identified]

class CommitRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal['Commit'] = Field(default='Commit', alias='@type')
    change: list[DataVersionRequest]

class PrimitiveConstraint(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    value: Union[str, int, float, bool, Identified]
    operator: Literal['=', '>', '<']
    inverse: bool
    property: str
    
class CompositeConstraint(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    constraint: list[PrimitiveConstraint]
    operator: Literal['and', 'or']

class Query(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='@id')
    owningProject: Identified
    select: list[str]
    where: Union[CompositeConstraint, PrimitiveConstraint]
    type: Literal['Query'] = Field(default='Query', alias='@type')

class QueryRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    select: list[str]
    where: PrimitiveConstraint
