# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from data_pipeline.initialization_vector import InitializationVector
from data_pipeline.message import CreateMessage


class TestInitializationVector(object):

    @pytest.fixture
    def vector_payload(self):
        return b'0000000000000000'

    @pytest.fixture
    def new_initialization_vector(
        self,
        vector_payload
    ):
        return InitializationVector(vector_payload)

    @pytest.fixture(params=[
        {'schema_id': 10},
        {'encoded_payload': bytes(10)}
    ])
    def invalid_arg_value(self, request):
        return request.param

    def test_create_vector_fails_with_bad_arg_values(self, invalid_arg_value):
        with pytest.raises(TypeError):
            InitializationVector(**invalid_arg_value)

    def test_initialization_vector_creation(self, new_initialization_vector):
        assert isinstance(new_initialization_vector, InitializationVector)
        assert isinstance(new_initialization_vector.avro_repr['payload'], bytes)

    def test_create_message_with_initialization_vector(
        self,
        vector_payload,
        new_initialization_vector
    ):
        test_message = CreateMessage(
            1,
            topic=str('my-topic'),
            payload=bytes(10),
            meta=[new_initialization_vector]
        )
        assert test_message.meta[0] == new_initialization_vector
