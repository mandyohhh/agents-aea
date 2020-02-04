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

"""This package contains the implementation of the error tasks."""
from aea.skills.tasks import Task


class ErrorTask(Task):
    """This class implements the error task."""

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """
        pass  # pragma: no cover

    def execute(self, *args, **kwargs) -> None:
        """
        Implement the task execution.

        :return: None
        """
        pass  # pragma: no cover

    def teardown(self) -> None:
        """
        Implement the task teardown.

        :return: None
        """
        pass  # pragma: no cover
