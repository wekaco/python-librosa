import pytest
import uuid
from unittest.mock import Mock

from lib.base import generator

class TestGenerator:
    def test_simple(self):
        mock = Mock()

        @generator('test_simple')
        def func(_):
            mock()

        g = func()
        g.send(None)

        mock.assert_called_once()

    def test_value(self):
        expected = uuid.uuid4()

        @generator('test_value')
        def func(actual):
            assert actual == expected

        g = func()
        g.send(expected)

    def test_args(self):
        init_arg_1 = uuid.uuid4()
        init_arg_2 = uuid.uuid4()

        send_arg = uuid.uuid4()

        @generator('test_args')
        def func(arg1, arg2, arg3):
            assert send_arg == arg1

            assert init_arg_1 == arg2
            assert init_arg_2 == arg3

        g = func(init_arg_1, init_arg_2)
        g.send(send_arg)

    def test_single_target(self):
        expected = uuid.uuid4()
        mock = Mock()

        @generator('source')
        def source(_):
            return expected

        @generator('sink')
        def sink(actual):
            mock()
            assert actual == expected

        g = source(targets=[ sink() ])
        g.send(None)
        mock.assert_called_once()

    def test_single_target(self):
        expected = uuid.uuid4()
        mock = Mock()

        @generator('source')
        def source(_):
            return expected

        @generator('sink')
        def sink(actual):
            mock()
            assert actual == expected

        g = source(targets=[ sink(), sink() ])
        g.send(None)
        assert mock.call_count == 2

    def test_collect(self):
        import random
        size = random.randint(2, 5)
        values = list(range(size))

        mock = Mock()

        @generator('collect', size=size)
        def collect(actual):
            mock()
            assert len(actual) == size
            assert actual == values

        g = collect()
        for i in values:
            g.send(i)

        mock.assert_called_once()
