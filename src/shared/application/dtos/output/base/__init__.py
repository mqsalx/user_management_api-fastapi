# /src/shared/application/dtos/output/base/__init__.py

from dataclasses import fields, is_dataclass, asdict
from typing import Any


class BaseOutputDTO:
    def __new__(cls, source: Any):
        source_dict = (
            source if isinstance(source, dict)
            else asdict(source) if is_dataclass(source)
            else source.model_dump() if hasattr(source, "model_dump")
            else source.dict() if hasattr(source, "dict")
            else {}
        )
        dto_fields = {field.name for field in fields(cls)}
        filtered = {k: source_dict[k] for k in dto_fields if k in source_dict}

        instance = super().__new__(cls)
        object.__setattr__(instance, "__dict__", filtered)
        return instance

