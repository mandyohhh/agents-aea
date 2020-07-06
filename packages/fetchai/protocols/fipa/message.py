# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2020 fetchai
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

"""This module contains fipa's message definition."""

import logging
from enum import Enum
from typing import Dict, Set, Tuple, cast

from aea.configurations.base import ProtocolId
from aea.protocols.base import Message

from packages.fetchai.protocols.fipa.custom_types import (
    Description as CustomDescription,
)
from packages.fetchai.protocols.fipa.custom_types import Query as CustomQuery

logger = logging.getLogger("aea.packages.fetchai.protocols.fipa.message")

DEFAULT_BODY_SIZE = 4


class FipaMessage(Message):
    """A protocol for FIPA ACL."""

    protocol_id = ProtocolId("fetchai", "fipa", "0.4.0")

    Description = CustomDescription

    Query = CustomQuery

    class Performative(Enum):
        """Performatives for the fipa protocol."""

        ACCEPT = "accept"
        ACCEPT_W_INFORM = "accept_w_inform"
        CFP = "cfp"
        DECLINE = "decline"
        INFORM = "inform"
        MATCH_ACCEPT = "match_accept"
        MATCH_ACCEPT_W_INFORM = "match_accept_w_inform"
        PROPOSE = "propose"

        def __str__(self):
            """Get the string representation."""
            return str(self.value)

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs,
    ):
        """
        Initialise an instance of FipaMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=FipaMessage.Performative(performative),
            **kwargs,
        )
        self._performatives = {
            "accept",
            "accept_w_inform",
            "cfp",
            "decline",
            "inform",
            "match_accept",
            "match_accept_w_inform",
            "propose",
        }

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        assert self.is_set("dialogue_reference"), "dialogue_reference is not set."
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        assert self.is_set("message_id"), "message_id is not set."
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # type: ignore # noqa: F821
        """Get the performative of the message."""
        assert self.is_set("performative"), "performative is not set."
        return cast(FipaMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        assert self.is_set("target"), "target is not set."
        return cast(int, self.get("target"))

    @property
    def info(self) -> Dict[str, str]:
        """Get the 'info' content from the message."""
        assert self.is_set("info"), "'info' content is not set."
        return cast(Dict[str, str], self.get("info"))

    @property
    def proposal(self) -> CustomDescription:
        """Get the 'proposal' content from the message."""
        assert self.is_set("proposal"), "'proposal' content is not set."
        return cast(CustomDescription, self.get("proposal"))

    @property
    def query(self) -> CustomQuery:
        """Get the 'query' content from the message."""
        assert self.is_set("query"), "'query' content is not set."
        return cast(CustomQuery, self.get("query"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the fipa protocol."""
        try:
            assert (
                type(self.dialogue_reference) == tuple
            ), "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                type(self.dialogue_reference)
            )
            assert (
                type(self.dialogue_reference[0]) == str
            ), "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                type(self.dialogue_reference[0])
            )
            assert (
                type(self.dialogue_reference[1]) == str
            ), "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                type(self.dialogue_reference[1])
            )
            assert (
                type(self.message_id) == int
            ), "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(
                type(self.message_id)
            )
            assert (
                type(self.target) == int
            ), "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(
                type(self.target)
            )

            # Light Protocol Rule 2
            # Check correct performative
            assert (
                type(self.performative) == FipaMessage.Performative
            ), "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                self.valid_performatives, self.performative
            )

            # Check correct contents
            actual_nb_of_contents = len(self.body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == FipaMessage.Performative.CFP:
                expected_nb_of_contents = 1
                assert (
                    type(self.query) == CustomQuery
                ), "Invalid type for content 'query'. Expected 'Query'. Found '{}'.".format(
                    type(self.query)
                )
            elif self.performative == FipaMessage.Performative.PROPOSE:
                expected_nb_of_contents = 1
                assert (
                    type(self.proposal) == CustomDescription
                ), "Invalid type for content 'proposal'. Expected 'Description'. Found '{}'.".format(
                    type(self.proposal)
                )
            elif self.performative == FipaMessage.Performative.ACCEPT_W_INFORM:
                expected_nb_of_contents = 1
                assert (
                    type(self.info) == dict
                ), "Invalid type for content 'info'. Expected 'dict'. Found '{}'.".format(
                    type(self.info)
                )
                for key_of_info, value_of_info in self.info.items():
                    assert (
                        type(key_of_info) == str
                    ), "Invalid type for dictionary keys in content 'info'. Expected 'str'. Found '{}'.".format(
                        type(key_of_info)
                    )
                    assert (
                        type(value_of_info) == str
                    ), "Invalid type for dictionary values in content 'info'. Expected 'str'. Found '{}'.".format(
                        type(value_of_info)
                    )
            elif self.performative == FipaMessage.Performative.MATCH_ACCEPT_W_INFORM:
                expected_nb_of_contents = 1
                assert (
                    type(self.info) == dict
                ), "Invalid type for content 'info'. Expected 'dict'. Found '{}'.".format(
                    type(self.info)
                )
                for key_of_info, value_of_info in self.info.items():
                    assert (
                        type(key_of_info) == str
                    ), "Invalid type for dictionary keys in content 'info'. Expected 'str'. Found '{}'.".format(
                        type(key_of_info)
                    )
                    assert (
                        type(value_of_info) == str
                    ), "Invalid type for dictionary values in content 'info'. Expected 'str'. Found '{}'.".format(
                        type(value_of_info)
                    )
            elif self.performative == FipaMessage.Performative.INFORM:
                expected_nb_of_contents = 1
                assert (
                    type(self.info) == dict
                ), "Invalid type for content 'info'. Expected 'dict'. Found '{}'.".format(
                    type(self.info)
                )
                for key_of_info, value_of_info in self.info.items():
                    assert (
                        type(key_of_info) == str
                    ), "Invalid type for dictionary keys in content 'info'. Expected 'str'. Found '{}'.".format(
                        type(key_of_info)
                    )
                    assert (
                        type(value_of_info) == str
                    ), "Invalid type for dictionary values in content 'info'. Expected 'str'. Found '{}'.".format(
                        type(value_of_info)
                    )
            elif self.performative == FipaMessage.Performative.ACCEPT:
                expected_nb_of_contents = 0
            elif self.performative == FipaMessage.Performative.DECLINE:
                expected_nb_of_contents = 0
            elif self.performative == FipaMessage.Performative.MATCH_ACCEPT:
                expected_nb_of_contents = 0

            # Check correct content count
            assert (
                expected_nb_of_contents == actual_nb_of_contents
            ), "Incorrect number of contents. Expected {}. Found {}".format(
                expected_nb_of_contents, actual_nb_of_contents
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                assert (
                    self.target == 0
                ), "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(
                    self.target
                )
            else:
                assert (
                    0 < self.target < self.message_id
                ), "Invalid 'target'. Expected an integer between 1 and {} inclusive. Found {}.".format(
                    self.message_id - 1, self.target,
                )
        except (AssertionError, ValueError, KeyError) as e:
            logger.error(str(e))
            return False

        return True
