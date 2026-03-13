import os
from typing import Any, Dict, Optional, Union
from fastmcp import FastMCP, Context
import httpx
from pydantic import BaseModel
from sysmlv2 import *

SYSMLV2_URL = os.getenv("SYSMLV2_URL", "http://localhost:8080")
READ_ONLY = os.getenv("READ_ONLY", "true").lower() in ("true", "1", "yes")
MCPPATH = os.getenv("MCPPATH", "/mcp")

mcp = FastMCP("SysMLv2 API")

def get_auth_header(ctx: Context) -> dict:
    """Extract Authorization header from request context."""
    headers = ctx.request_context.request.headers
    auth_header = headers.get("authorization") or headers.get("Authorization")
    if auth_header:
        return {"Authorization": auth_header}
    return {}

async def make_request(
    method: str, 
    path: str, 
    ctx: Context,
    query_params: Optional[Dict] = None, 
    body: Optional[Union[Dict, BaseModel, str]] = None
) -> Any:
    """Make an HTTP request to the SysMLv2 API."""
    if not SYSMLV2_URL:
        raise ValueError("SYSMLV2_URL environment variable is not set")
    
    full_url = f"{SYSMLV2_URL.rstrip('/')}{path}"
    headers = get_auth_header(ctx)
    headers["Content-Type"] = "application/json"
    
    json = body.model_dump(by_alias=True) if hasattr(body, 'model_dump') else body
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                response = await client.get(full_url, headers=headers, params=query_params)
            elif method == "POST":
                response = await client.post(full_url, headers=headers, params=query_params, json=json)
            elif method == "PUT":
                response = await client.put(full_url, headers=headers, params=query_params, json=json)
            elif method == "DELETE":
                response = await client.delete(full_url, headers=headers, params=query_params)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            response.raise_for_status()
            
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            else:
                return response.text
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP {e.response.status_code}",
                "message": e.response.text,
                "url": str(e.request.url)
            }
        except Exception as e:
            return {"error": str(e)}


#@mcp.tool()
#async def get_datatypes(pageAfter: Optional[str] = None, pageBefore: Optional[str] = None, pageSize: Optional[int] = None) -> Dict[str, Any]:
#    """Get datatypes"""
#    params = {}
#    if pageAfter: params["pageAfter"] = pageAfter
#    if pageBefore: params["pageBefore"] = pageBefore
#    if pageSize: params["pageSize"] = pageSize
#    return await make_request("GET", "/meta/datatypes", query_params=params)

#@mcp.tool()
#async def get_datatype_by_id(datatypeId: str) -> Dict[str, Any]:
#    """Get datatype by ID"""
#    return await make_request("GET", f"/meta/datatypes/{datatypeId}")

@mcp.tool()
async def get_projects(ctx: Context) -> list[Project]:
    """Get projects"""
    return await make_request("GET", "/projects", ctx)


@mcp.tool()
async def get_project_by_id(projectId: str, ctx: Context) -> Project:
    """Get project by project id"""
    return await make_request("GET", f"/projects/{projectId}", ctx)

if not READ_ONLY:
    @mcp.tool()
    async def post_project(ctx: Context, body: ProjectRequest) -> Project:
        """Create project"""
        return await make_request("POST", "/projects", ctx, body=body)

    @mcp.tool()
    async def put_project_by_id(projectId: str, ctx: Context, body: ProjectRequest) -> Project:
        """Update project by project id"""
        return await make_request("PUT", f"/projects/{projectId}", ctx, body=body)

    @mcp.tool()
    async def delete_project_by_id(projectId: str, ctx: Context) -> Project:
        """Delete project by project id"""
        return await make_request("DELETE", f"/projects/{projectId}", ctx)

@mcp.tool()
async def get_branches_by_project(projectId: str, ctx: Context) -> list[Branch]:
    """Get branches by project id"""
    return await make_request("GET", f"/projects/{projectId}/branches", ctx)

@mcp.tool()
async def get_branches_by_project_and_id(projectId: str, branchId: str, ctx: Context) -> Branch:
    """Get branch by project and branch id"""
    return await make_request("GET", f"/projects/{projectId}/branches/{branchId}", ctx)

if not READ_ONLY:
    @mcp.tool()
    async def post_branch_by_project(projectId: str, ctx: Context, body: BranchRequest) -> Branch:
        """Create branch in project"""
        return await make_request("POST", f"/projects/{projectId}/branches", ctx, body=body)

    @mcp.tool()
    async def delete_branch_by_project_and_id(projectId: str, branchId: str, ctx: Context) -> Branch:
        """Delete branch by project and branch id"""
        return await make_request("DELETE", f"/projects/{projectId}/branches/{branchId}", ctx)

    #@mcp.tool()
    #async def merge(projectId: str, targetBranchId: str, ctx: Context, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    #    """Merge source commit(s) into a target branch"""
    #    return await make_request("POST", f"/projects/{projectId}/branches/{targetBranchId}/merge", ctx, body=body)

@mcp.tool()
async def get_commits_by_project(projectId: str, ctx: Context) -> list[Commit]:
    """Get commits by project id"""
    return await make_request("GET", f"/projects/{projectId}/commits", ctx)

@mcp.tool()
async def get_commit_by_project_and_id(projectId: str, commitId: str, ctx: Context) -> Commit:
    """Get commit by project and commit id"""
    return await make_request("GET", f"/projects/{projectId}/commits/{commitId}", ctx)

if not READ_ONLY:
    @mcp.tool()
    async def post_commit_by_project(projectId: str, ctx: Context, body: CommitRequest, branchId: Optional[str]) -> Commit:
        """Create commit in project, if branch id isn't specified commit will be made on project's default branch. To delete an element, include the element's identity object with @id, without a payload, in the change list"""
        params = {}
        if branchId: params["branchId"] = branchId
        return await make_request("POST", f"/projects/{projectId}/commits", ctx, body=body.model_dump(), query_params=params)


#@mcp.tool()
#async def get_changes_by_project_commit(projectId: str, commitId: str, ctx: Context, commitId_query: Optional[str] = None) -> Dict[str, Any]:
#    """Get changes by project and commit"""
#    params = {}
#    if commitId_query: params["commitId"] = commitId_query
#    return await make_request("GET", f"/projects/{projectId}/commits/{commitId}/changes", ctx, query_params=params)

#@mcp.tool()
#async def get_change_by_project_commit_id(projectId: str, commitId: str, changeId: str, ctx: Context) -> Dict[str, Any]:
#    """Get change by project, commit and ID"""
#    return await make_request("GET", f"/projects/{projectId}/commits/{commitId}/changes/{changeId}", ctx)

@mcp.tool()
async def get_elements_by_project_commit(projectId: str, commitId: str, ctx: Context) -> list[dict]:
    """Get elements by project and commit id"""
    return await make_request("GET", f"/projects/{projectId}/commits/{commitId}/elements", ctx)

@mcp.tool()
async def get_element_by_project_commit_id(projectId: str, commitId: str, elementId: str, ctx: Context) -> Dict[str, Any]:
    """Get element by project, commit and element id"""
    return await make_request("GET", f"/projects/{projectId}/commits/{commitId}/elements/{elementId}", ctx)

#@mcp.tool()
#async def get_project_usage_by_project_commit_element(projectId: str, commitId: str, elementId: str, ctx: Context) -> Dict[str, Any]:
#    """Get ProjectUsage that originates the provided element"""
#    return await make_request("GET", f"/projects/{projectId}/commits/{commitId}/elements/{elementId}/projectUsage", ctx)

@mcp.tool()
async def get_relationships_by_project_commit_related_element(projectId: str, commitId: str, relatedElementId: str, ctx: Context, direction: Optional[Literal['in', 'out', 'both']] = None) -> list[dict]:
    """Get relationships for a related element, direction can be 'in', 'out', or 'both'"""
    params = {}
    if direction: params["direction"] = direction
    return await make_request("GET", f"/projects/{projectId}/commits/{commitId}/elements/{relatedElementId}/relationships", ctx, query_params=params)

@mcp.tool()
async def get_roots_by_project_commit(projectId: str, commitId: str, ctx: Context) -> list[dict]:
    """Get root elements by project and commit id"""
    return await make_request("GET", f"/projects/{projectId}/commits/{commitId}/roots", ctx)

#@mcp.tool()
#async def diff(projectId: str, compareCommitId: str, ctx: Context, commitId: Optional[str] = None) -> Dict[str, Any]:
#    """Compare two commits"""
#    params = {}
#    if commitId: params["commitId"] = commitId
#    return await make_request("GET", f"/projects/{projectId}/commits/{compareCommitId}/diff", ctx, query_params=params)

@mcp.tool()
async def get_queries_by_project(projectId: str, ctx: Context) -> list[Query]:
    """Get queries by project id"""
    return await make_request("GET", f"/projects/{projectId}/queries", ctx)

@mcp.tool()
async def get_query_by_project_and_id(projectId: str, queryId: str, ctx: Context) -> Query:
    """Get query by project and query id"""
    return await make_request("GET", f"/projects/{projectId}/queries/{queryId}", ctx)

@mcp.tool()
async def get_query_results_by_project_id_query_id(projectId: str, queryId: str, ctx: Context, commitId: Optional[str] = None) -> list[dict]:
    """Get query results by project and query id, if commit id isn't provided uses head of default branch"""
    params = {}
    if commitId: params["commitId"] = commitId
    return await make_request("GET", f"/projects/{projectId}/queries/{queryId}/results", ctx, query_params=params)

@mcp.tool()
async def get_query_results_by_project_id_query(projectId: str, query: QueryRequest, ctx: Context, commitId: Optional[str] = None) -> list[dict]:
    """Get query results by project and given query, if commit id isn't provided uses head of default branch"""
    params = {}
    if commitId: params["commitId"] = commitId
    return await make_request("POST", f"/projects/{projectId}/query-results", ctx, body=query, query_params=params)

if not READ_ONLY:
    @mcp.tool()
    async def post_query_by_project(projectId: str, ctx: Context, body: QueryRequest) -> Query:
        """Create query in project"""
        return await make_request("POST", f"/projects/{projectId}/queries", ctx, body=body)

    @mcp.tool()
    async def put_query_by_project_and_id(projectId: str, queryId: str, ctx: Context, body: QueryRequest) -> Query:
        """Update query in project and by query id"""
        return await make_request("PUT", f"/projects/{projectId}/queries/{queryId}", ctx, body=body)

    @mcp.tool()
    async def delete_query_by_project_and_id(projectId: str, queryId: str, ctx: Context) -> Query:
        """Delete query by project and query id"""
        return await make_request("DELETE", f"/projects/{projectId}/queries/{queryId}", ctx)


@mcp.tool()
async def get_tags_by_project(projectId: str, ctx: Context) -> list[Tag]:
    """Get tags by project id"""
    return await make_request("GET", f"/projects/{projectId}/tags", ctx)

@mcp.tool()
async def get_tag_by_project_and_id(projectId: str, tagId: str, ctx: Context) -> Tag:
    """Get tag by project and tag id"""
    return await make_request("GET", f"/projects/{projectId}/tags/{tagId}", ctx)

if not READ_ONLY:
    @mcp.tool()
    async def post_tag_by_project(projectId: str, ctx: Context, body: TagRequest) -> Tag:
        """Create tag in project"""
        return await make_request("POST", f"/projects/{projectId}/tags", ctx, body=body)

    @mcp.tool()
    async def delete_tag_by_project_and_id(projectId: str, tagId: str, ctx: Context) -> Tag:
        """Delete tag by project and tag id"""
        return await make_request("DELETE", f"/projects/{projectId}/tags/{tagId}", ctx)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000, path=MCPPATH)
