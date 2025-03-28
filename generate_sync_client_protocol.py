import inspect
from decimal import Decimal
from enum import Enum

from typing import Any, Sequence, get_args, get_origin, Union
import collections.abc

import architect_py.async_client

from architect_py.graphql_client.base_model import UnsetType


def format_type_hint_with_generics(type_hint) -> str:
    """
    Format a type hint to a string representation with support for generic types like list[str].
    """

    if type_hint == inspect.Parameter.empty:
        return "Any"

    origin = get_origin(type_hint)
    if origin is Union:
        args = get_args(type_hint)
        if type(None) in args:
            if len(args) == 2:
                # Handle Optional[X]
                non_none_type = args[0] if args[1] is type(None) else args[1]
                return f"Optional[{format_type_hint_with_generics(non_none_type)}]"
        return (
            f"Union[{', '.join(format_type_hint_with_generics(arg) for arg in args)}]"
        ).replace("NoneType", "None")

    elif origin in (Sequence, collections.abc.Sequence):
        args = get_args(type_hint)
        if args:
            return f"Sequence[{format_type_hint_with_generics(args[0])}]"
        return "Sequence[Any]"

    elif origin is list:
        args = get_args(type_hint)
        if args:
            return f"list[{format_type_hint_with_generics(args[0])}]"
        return "list[Any]"

    elif origin is dict:
        args = get_args(type_hint)
        if len(args) == 2:
            return f"dict[{format_type_hint_with_generics(args[0])}, {format_type_hint_with_generics(args[1])}]"
        return "dict[Any, Any]"

    elif origin is tuple:
        args = get_args(type_hint)
        if args:
            return f"tuple[{', '.join(format_type_hint_with_generics(arg) for arg in args)}]"
        return "tuple[Any, ...]"

    try:
        return type_hint.__name__
    except AttributeError:
        return str(type_hint)


def autogenerate_protocol(cls) -> str:
    """
    Autogenerate a Protocol for the given class for use in static typing.
    Args:
        cls: The class to generate a Protocol for.
    Returns:
        A string representing the Protocol definition.
    """
    protocol_name = f"{cls.__name__}Protocol"
    methods = {}
    method_decorators = {}
    attributes = {}

    # Inspect class members
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        if callable(member):
            # Collect methods
            signature = inspect.signature(member)
            methods[name] = signature

            raw_member = inspect.getattr_static(cls, name)
            decorators = []
            if isinstance(raw_member, staticmethod):
                decorators.append("@staticmethod")
            elif isinstance(raw_member, classmethod):
                decorators.append("@classmethod")
            method_decorators[name] = decorators
        elif not inspect.isroutine(member):
            # Collect attributes
            attributes[name] = getattr(cls, name, Any)

    def format_default(value) -> str:
        """
        Format the default value for parameters. Handles special types.
        """
        if isinstance(value, Enum):
            return f"{value.__class__.__name__}.{value.name}"
        elif isinstance(value, (int, float, str, bool, type(None))):
            return repr(value)
        elif isinstance(value, Decimal):
            return f"Decimal('{value}')"
        elif isinstance(value, UnsetType):
            return "UNSET"
        return type(value).__name__

    protocol_lines = [
        "# fmt: off\n",
        "# mypy: ignore-errors\n",
        "# Autogenerated from generate_protocol.py\n",
        "# If you are here for function definitions, please refer to architect_py/async_cline.py",
        "# This file is so that the sync client has good type hinting",
        "# It is not used for anything else",
        "# For maintainers: ensure that the types in this file are correct for correct type hinting",
        "\n",
        # "from architect_py.grpc_client.definitions import *",
        "from architect_py.graphql_client import *",
        "from architect_py.async_client import *",
        "\n",
        f"class {protocol_name}:",
    ]

    # Add attributes
    for attr_name, attr_type in attributes.items():
        protocol_lines.append(
            f"    {attr_name}: {format_type_hint_with_generics(attr_type)}"
        )

    # Add methods
    for name, signature in methods.items():
        if "subscribe" in name:
            continue

        if name == "create":
            continue

        # for decorators like @staticmethod and @classmethod
        if name in method_decorators:
            for deco in method_decorators[name]:
                protocol_lines.append(f"    {deco}")

        params = []
        keyword_only = False
        for param_name, param in signature.parameters.items():
            if param_name == "self":
                params.append("self")
                continue

            param_type = format_type_hint_with_generics(param.annotation)
            if param.kind == inspect.Parameter.POSITIONAL_ONLY:
                params.append(f"{param_name}: {param_type}")
            elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                if param.default != inspect.Parameter.empty:
                    params.append(
                        f"{param_name}: {param_type} = {format_default(param.default)}"
                    )
                else:
                    params.append(f"{param_name}: {param_type}")
            elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                params.append(f"*{param_name}: {param_type}")
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                if not keyword_only:
                    params.append("*")  # Indicate start of keyword-only arguments
                    keyword_only = True
                if param.default != inspect.Parameter.empty:
                    params.append(
                        f"{param_name}: {param_type} = {format_default(param.default)}"
                    )
                else:
                    params.append(f"{param_name}: {param_type}")
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                params.append(f"**{param_name}: {param_type}")

        params_str = ", ".join(params)
        return_type = format_type_hint_with_generics(signature.return_annotation)
        protocol_lines.append(f"    def {name}({params_str}) -> {return_type}: ...")

    return "\n".join(protocol_lines)


if __name__ == "__main__":
    print(autogenerate_protocol(architect_py.async_client.AsyncClient))
