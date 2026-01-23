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

import datetime
import json
import pathlib
from typing import TYPE_CHECKING

import pydantic
import pytest

import atr.cache as cache

if TYPE_CHECKING:
    from pytest import MonkeyPatch


class _MockConfig:
    def __init__(self, state_dir: pathlib.Path):
        self.STATE_DIR = str(state_dir)


@pytest.fixture
def state_dir(tmp_path: pathlib.Path, monkeypatch: "MonkeyPatch") -> pathlib.Path:
    monkeypatch.setattr("atr.config.get", lambda: _MockConfig(tmp_path))
    return tmp_path


def test_admins_cache_rejects_missing_admins():
    with pytest.raises(pydantic.ValidationError):
        cache.AdminsCache.model_validate({"refreshed": "2025-01-01T00:00:00Z"})


def test_admins_cache_rejects_missing_refreshed():
    with pytest.raises(pydantic.ValidationError):
        cache.AdminsCache.model_validate({"admins": ["alice"]})


def test_admins_cache_roundtrip_json():
    original = cache.AdminsCache(
        refreshed=datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.UTC),
        admins=frozenset({"alice", "bob", "charlie"}),
    )
    json_str = original.model_dump_json()
    restored = cache.AdminsCache.model_validate_json(json_str)
    assert restored.refreshed == original.refreshed
    assert restored.admins == original.admins


def test_admins_cache_serializes_to_json():
    data = cache.AdminsCache(
        refreshed=datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.UTC),
        admins=frozenset({"alice", "bob"}),
    )
    json_str = data.model_dump_json()
    parsed = json.loads(json_str)
    assert "refreshed" in parsed
    assert "admins" in parsed
    assert set(parsed["admins"]) == {"alice", "bob"}


def test_admins_cache_validates_with_good_data():
    data = cache.AdminsCache(
        refreshed=datetime.datetime.now(datetime.UTC),
        admins=frozenset({"alice", "bob"}),
    )
    assert isinstance(data.refreshed, datetime.datetime)
    assert data.admins == frozenset({"alice", "bob"})


@pytest.mark.asyncio
async def test_admins_read_from_file_returns_none_for_invalid_json(state_dir: pathlib.Path):
    cache_path = state_dir / "cache" / "admins.json"
    cache_path.parent.mkdir(parents=True)
    cache_path.write_text("not valid json {{{")
    result = await cache.admins_read_from_file()
    assert result is None


@pytest.mark.asyncio
async def test_admins_read_from_file_returns_none_for_invalid_schema(state_dir: pathlib.Path):
    cache_path = state_dir / "cache" / "admins.json"
    cache_path.parent.mkdir(parents=True)
    cache_path.write_text('{"wrong_field": "value"}')
    result = await cache.admins_read_from_file()
    assert result is None


@pytest.mark.asyncio
async def test_admins_read_from_file_returns_none_for_missing(state_dir: pathlib.Path):
    result = await cache.admins_read_from_file()
    assert result is None


@pytest.mark.asyncio
async def test_admins_save_and_read_roundtrip(state_dir: pathlib.Path):
    original_admins = frozenset({"alice", "bob", "charlie"})
    await cache.admins_save_to_file(original_admins)
    result = await cache.admins_read_from_file()
    assert result is not None
    assert result.admins == original_admins


@pytest.mark.asyncio
async def test_admins_save_to_file_creates_file(state_dir: pathlib.Path):
    admins = frozenset({"alice", "bob"})
    await cache.admins_save_to_file(admins)
    cache_path = state_dir / "cache" / "admins.json"
    assert cache_path.exists()


@pytest.mark.asyncio
async def test_admins_save_to_file_creates_parent_dirs(state_dir: pathlib.Path):
    cache_dir = state_dir / "cache"
    assert not cache_dir.exists()
    await cache.admins_save_to_file(frozenset({"alice"}))
    assert cache_dir.exists()
    assert cache_dir.is_dir()
