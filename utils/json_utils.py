from jsonschema import validate, ValidationError
from pydantic import BaseModel
from typing import Union, Type
import json

def validate_json(json_str: str, 
                  schema: Union[Type[BaseModel], dict], 
                  strip:bool = True):
    """
    Validate a JSON string against either a Pydantic model or a JSON Schema dict.
    Returns the validated object if valid, or raises an exception if not.
    If providing a Pydantic model, expect a return in the same type as the schema provided.
    If providing a JSON schema dict, expect a dictionary return type.
    """
    if strip == True: json_str = strip_json_code_fence(json_str)
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        return _validate_json_with_pydantic(json_str, schema)
    else:
        return _validate_json_with_jsonschema(json_str, schema)

def _validate_json_with_pydantic(json_str: str, schema: Type[BaseModel]) -> BaseModel:
    try:
        json_dict = json.loads(json_str)
        return schema(**json_dict)
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Unable to validate JSON string with schema type: {schema.__name__}. Full string:\n{json_str}\nError: {e}")
        raise e

def _validate_json_with_jsonschema(json_str: str, schema: dict) -> dict:
    try:
        json_dict = json.loads(json_str)
        validate(instance=json_dict, schema=schema)
        return json_dict
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Unable to validate JSON string with schema type:\n{schema}\nFull string:\n{json_str}\nError: {e}")
        raise e
    
def strip_json_code_fence(json_str: str) -> str:
    """
    Removes ```json or ``` wrappers from LLM responses.
    """
    if json_str.startswith("```json"):
        json_str = json_str.strip()[7:]
    elif json_str.startswith("```"):
        json_str = json_str.strip()[3:]
    return json_str.rstrip("```").strip()