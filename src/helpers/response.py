import os
from pathlib import Path
from typing import Dict

import jinja2
from fastapi import HTTPException


def error(message: str = None, data: dict = None, code: int = 400) -> dict:
    """
    Create exception object

    Args:
        message: Error message. Defaults to None.
        data: Defaults to None.

    Returns:
        errors
    """
    message = message or "Something went wrong."
    detail = {"msg": str(message), "loc": [], "type": None}
    if data:
        detail["data"] = data
    return HTTPException(status_code=code, detail=[detail])


def response_structure(data, total_rows: int = None) -> Dict:
    response = {"objects": data}
    if total_rows is not None:
        response["total_rows"] = total_rows
    return response

JINJA2_TEMPLATE_PATH = os.path.join(
    str(Path(__file__).parent.parent.parent), "src", "templates"
)
jinja2_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [JINJA2_TEMPLATE_PATH, os.path.join("..", "templates", "")]
    ),
    autoescape=jinja2.select_autoescape(),
)
