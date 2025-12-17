#!/usr/bin/env python3

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
import pathlib
import sys
from typing import Final

_MAX_AGE_DAYS: Final[int] = 30


def main() -> None:
    lock_path = pathlib.Path("uv.lock")
    if not lock_path.exists():
        print("ERROR: uv.lock not found", file=sys.stderr)
        sys.exit(1)

    exclude_newer = _parse_exclude_newer(lock_path)
    if exclude_newer is None:
        print("ERROR: No exclude-newer timestamp in uv.lock", file=sys.stderr)
        print("Run: make update-deps", file=sys.stderr)
        sys.exit(1)

    timestamp = _parse_timestamp(exclude_newer)
    if timestamp is None:
        print(f"ERROR: Could not parse timestamp: {exclude_newer}", file=sys.stderr)
        sys.exit(1)

    now = datetime.datetime.now(datetime.UTC)
    age = now - timestamp

    if age > datetime.timedelta(days=_MAX_AGE_DAYS):
        print(f"ERROR: Dependencies are {age.days} days old (the limit is {_MAX_AGE_DAYS} days)", file=sys.stderr)
        print(f"Last updated: {exclude_newer}", file=sys.stderr)
        print("Run: make update-deps", file=sys.stderr)
        sys.exit(1)

    print(f"OK: Dependencies are {age.days} days old (the limit is {_MAX_AGE_DAYS} days)")


def _parse_exclude_newer(lock_path: pathlib.Path) -> str | None:
    for line in lock_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("exclude-newer"):
            _, _, value = line.partition("=")
            return value.strip().strip('"')
    return None


def _parse_timestamp(timestamp_str: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    except ValueError:
        return None


if __name__ == "__main__":
    main()
