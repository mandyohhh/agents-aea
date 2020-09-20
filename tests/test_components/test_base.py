# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains tests for aea/components/base.py"""
from pathlib import Path

import pytest

from aea.components.base import Component, load_aea_package
from aea.configurations.base import ConnectionConfig, ProtocolConfig
from tests.conftest import ROOT_DIR


class TestComponentProperties:
    """Test accessibility of component properties."""

    def setup_class(self):
        """Setup test."""
        self.configuration = ProtocolConfig("name", "author", "0.1.0")
        self.component = Component(configuration=self.configuration)
        self.directory = Path()
        self.component._directory = self.directory

    def test_component_type(self):
        """Test component type attribute."""
        assert self.component.component_type == self.configuration.component_type

    def test_is_vendor(self):
        """Test component type attribute."""
        assert self.component.is_vendor is False

    def test_prefix_import_path(self):
        """Test component type attribute."""
        assert self.component.prefix_import_path == "packages.author.protocols.name"

    def test_component_id(self):
        """Test component id."""
        assert self.component.component_id == self.configuration.component_id

    def test_public_id(self):
        """Test public id."""
        assert self.component.public_id == self.configuration.public_id

    def test_directory(self):
        """Test directory."""
        assert self.component.directory == self.directory


def test_directory_setter():
    """Test directory."""
    configuration = ProtocolConfig("author", "name", "0.1.0")
    component = Component(configuration=configuration)

    with pytest.raises(ValueError):
        component.directory

    new_path = Path("new_path")
    component.directory = new_path
    assert component.directory == new_path


def test_load_aea_package():
    """Test aea package load."""
    config = ConnectionConfig("http_client", "fetchai", "0.5.0")
    config.directory = Path(ROOT_DIR) / "packages"
    load_aea_package(config)
