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

"""This module contains the tests of the ethereum module."""
from unittest.mock import MagicMock

from aea.crypto.cosmos import CosmosApi, CosmosCrypto

from tests.conftest import COSMOS_PRIVATE_KEY_PATH, COSMOS_TESTNET_CONFIG


def test_creation():
    """Test the creation of the crypto_objects."""
    assert CosmosCrypto(), "Did not manage to initialise the crypto module"
    assert CosmosCrypto(
        COSMOS_PRIVATE_KEY_PATH
    ), "Did not manage to load the cosmos private key"


def test_initialization():
    """Test the initialisation of the variables."""
    account = CosmosCrypto()
    assert account.entity is not None, "The property must return the account."
    assert (
        account.address is not None
    ), "After creation the display address must not be None"
    assert account.address.startswith("cosmos")
    assert (
        account.public_key is not None
    ), "After creation the public key must no be None"


def test_sign_and_recover_message():
    """Test the signing and the recovery of a message."""
    account = CosmosCrypto(COSMOS_PRIVATE_KEY_PATH)
    sign_bytes = account.sign_message(message=b"hello")
    assert len(sign_bytes) > 0, "The len(signature) must not be 0"
    recovered_addresses = CosmosApi.recover_message(
        message=b"hello", signature=sign_bytes
    )
    assert (
        account.address in recovered_addresses
    ), "Failed to recover the correct address."


def test_get_hash():
    """Test the get hash functionality."""
    expected_hash = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    hash_ = CosmosApi.get_hash(message=b"hello")
    assert expected_hash == hash_


def test_dump_positive():
    """Test dump."""
    account = CosmosCrypto(COSMOS_PRIVATE_KEY_PATH)
    account.dump(MagicMock())


def test_api_creation():
    """Test api instantiation."""
    assert CosmosApi(**COSMOS_TESTNET_CONFIG), "Failed to initialise the api"


def test_api_none():
    """Test the "api" of the cryptoApi is none."""
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    assert cosmos_api.api is None, "The api property is not None."


def test_generate_nonce():
    """Test generate nonce."""
    nonce = CosmosApi.generate_tx_nonce(
        seller="some_seller_addr", client="some_buyer_addr"
    )
    assert len(nonce) > 0 and int(
        nonce, 16
    ), "The len(nonce) must not be 0 and must be hex"


def test_validate_address():
    """Test the is_valid_address functionality."""
    account = CosmosCrypto()
    assert CosmosApi.is_valid_address(account.address)
    assert not CosmosApi.is_valid_address(account.address + "wrong")
