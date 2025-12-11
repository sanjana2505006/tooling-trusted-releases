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

from playwright.sync_api import Locator, Page


def get_curl_command_text(page: Page) -> Locator:
    """Return the curl command text locator."""
    return page.locator("#curl-command")


def get_curl_copy_button(page: Page) -> Locator:
    """Return the curl command copy button locator."""
    return page.locator('button.atr-copy-btn[data-clipboard-target="#curl-command"]')


def get_rsync_command_text(page: Page) -> Locator:
    """Return the rsync command text locator."""
    return page.locator("#rsync-command")


def get_rsync_copy_button(page: Page) -> Locator:
    """Return the rsync command copy button locator."""
    return page.locator('button.atr-copy-btn[data-clipboard-target="#rsync-command"]')
