# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import annotations

import enum
from typing import Any

import pydantic

from .base import Strict


class Category(enum.Enum):
    A = enum.auto()
    B = enum.auto()
    X = enum.auto()

    def __str__(self):
        return self.name


class Issue(Strict):
    component_name: str
    component_version: str | None
    component_type: str | None = None
    license_expression: str
    category: Category
    any_unknown: bool = False
    scope: str | None = None

    @pydantic.field_validator("category", mode="before")
    @classmethod
    def _coerce_property(cls, value: Any) -> Category:
        return value if isinstance(value, Category) else Category(value)

    def __str__(self):
        type_str = "Component" if (self.component_type is None) else self.component_type
        version_str = f"@{self.component_version}" if (self.component_version != "UNKNOWN") else ""
        return f"{type_str} {self.component_name}{version_str} declares license {self.license_expression}"
