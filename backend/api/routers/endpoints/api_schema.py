from fastapi import APIRouter, FastAPI, Request


router = APIRouter()

def gather_referenced_components(schema, all_components, gathered_components):
    if "$ref" in schema:
        ref = schema["$ref"].split("/")[3]  # Extract the component name
        if ref not in gathered_components:
            gathered_components.add(ref)
            ref_schema = all_components.get(ref, {})
            gather_referenced_components(ref_schema, all_components, gathered_components)
    elif "properties" in schema:
        for prop_schema in schema["properties"].values():
            gather_referenced_components(prop_schema, all_components, gathered_components)
    elif "items" in schema:
        gather_referenced_components(schema["items"], all_components, gathered_components)
    elif "anyOf" in schema:
        for any_of_schema in schema["anyOf"]:
            gather_referenced_components(any_of_schema, all_components, gathered_components)
    elif "allOf" in schema:
        for all_of_schema in schema["allOf"]:
            gather_referenced_components(all_of_schema, all_components, gathered_components)

def get_filtered_schema(app: FastAPI, router_prefixes: list[str] = None) -> dict:
    openapi_schema = app.openapi()
    if not router_prefixes:
        filtered_paths = {path: value for path, value in openapi_schema["paths"].items()}
    else:
        filtered_paths = {path: value for path, value in openapi_schema["paths"].items() if any(path.startswith(prefix) for prefix in router_prefixes)}
    
    # Remove tags from paths
    for path_item in filtered_paths.values():
        for method in path_item.values():
            method.pop("tags", None)

    #Remove the header parameter from the paths
    for path_item in filtered_paths.values():
        for method in path_item.values():
            method.pop("parameters", None)


    # Find referenced components in paths
    referenced_components = set()
    for path_item in filtered_paths.values():
        for method in path_item.values():
            for response in method.get("responses", {}).values():
                content = response.get("content", {})
                for media_type in content.values():
                    schema = media_type.get("schema", {})
                    gather_referenced_components(schema, openapi_schema["components"]["schemas"], referenced_components)
            for body in method.get("requestBody", {}).get("content", {}).values():
                schema = body.get("schema", {})
                gather_referenced_components(schema, openapi_schema["components"]["schemas"], referenced_components)
    
    # Filter components
    filtered_components = {comp: value for comp, value in openapi_schema["components"]["schemas"].items() if comp in referenced_components}
    return {"openapi": openapi_schema["openapi"], "info": openapi_schema["info"], "paths": filtered_paths, "components": {"schemas": filtered_components}}


@router.get("/")
async def get_complete_schema(request: Request):
    schemes = get_filtered_schema(request.app)
    servers =[{"url": "https://obsgpt.kon.foo"}]
    schemes["servers"] = servers
    del schemes["paths"]["/api/schema/"]
    # schemes["paths"]["/api/solve/{quest_id}"]["post"]["x-openai-isConsequential"] = False
    schemes["info"]["title"] = "Obsidian GPT Backend"
    return schemes


# @router.get("/solve/{quest_id}")
# async def get_solve_schema(request: Request, db: deps.SessionDep, quest_id: uuid.UUID):
#     quest = crud.quests.get(db, quest_id)
#     if quest is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quest not found")
#     scheme = get_filtered_schema(request.app, ["/api/solve"])
#     servers =[{"url": "https://caqpoc.luona.dev"}]
#     scheme["servers"] = servers
#     scheme["paths"]["/api/solve/{quest_id}"]["post"]["x-openai-isConsequential"] = False
#     scheme["info"]["title"] = quest.project.name
#     scheme["paths"][f"/api/solve/{quest.id}"] = scheme["paths"]["/api/solve/{quest_id}"]
#     del scheme["paths"]["/api/solve/{quest_id}"]
#     return scheme

# @router.get("/entrance/{project_id}")
# async def get_entrance_schema(request: Request, db: deps.SessionDep, project_id: uuid.UUID):
#     schemes = get_filtered_schema(request.app, ["/api/entrance/register", "/api/entrance/next", "/api/entrance/leaderboard"])
#     project = crud.projects.get(db, project_id)
#     if project is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
#     # TODO: Make this dynamic
#     servers =[{"url": "https://caqpoc.luona.dev"}]
#     schemes["servers"] = servers
#     schemes["info"]["title"] = project.name

#     schemes["paths"][f"/api/entrance/leaderboard/{project_id}"] = schemes["paths"]["/api/entrance/leaderboard/{project_id}"]
#     del schemes["paths"]["/api/entrance/leaderboard/{project_id}"]
#     schemes["paths"][f"/api/entrance/leaderboard/{project_id}"]["get"]["x-openai-isConsequential"] = False
#     schemes["paths"]["/api/entrance/next"]["post"]["x-openai-isConsequential"] = False
#     return schemes
