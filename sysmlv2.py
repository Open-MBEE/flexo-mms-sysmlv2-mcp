from pydantic.dataclasses import dataclass
from pydantic import Field
from typing import Optional, Literal

@dataclass
class Identified:
    id: str = Field(alias='@id')

@dataclass
class BranchRequest:
    name: str
    head: Identified

@dataclass
class Branch:
    id: str = Field(alias='@id')
    type: str = Field(alias='@type', const=True, default="Branch")
    name: str
    created: str
    head: Identified
    owningProject: Identified
    referencedCommit: Identified

@dataclass
class Project:
    id: str = Field(alias='@id')
    type: str = Field(alias='@type', const=True, default="Project")
    name: str
    created: str
    description: str
    defaultBranch: Identified

@dataclass
class ProjectRequest:
    name: str
    description: Optional[str]
    defaultBranch: Optional[Identified]


@dataclass
class Tag:
    id: str = Field(alias='@id')
    type: str = Field(alias='@type', const=True, default="Tag")
    name: str
    created: str
    referencedCommit: Identified
    owningProject: Identified
    taggedCommit: Identified

@dataclass
class TagRequest:
    name: str
    taggedCommit: Identified

@dataclass
class Commit:
    id: str = Field(alias='@id')
    type: str = Field(alias='@type', const=True, default="Commit")
    created: str
    owningProject: Identified
    description: str
    previousCommit: Optional[Identified]

@dataclass
class PrimitiveConstraint:
    value: str | int | float | bool | Identified
    operator: Literal['=', '>', '<']
    inverse: bool
    property: str
    
@dataclass
class CompositeConstraint:
    constraint: list[PrimitiveConstraint]
    operator: Literal['and', 'or']

@dataclass
class Query:
    id: str = Field(alias='@id')
    type: str = Field(alias='@type', const=True, default="Query")
    owningProject: Identified
    select: list[str]
    where: CompositeConstraint | PrimitiveConstraint
