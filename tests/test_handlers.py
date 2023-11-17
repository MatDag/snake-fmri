"""Tests for the handler interface."""
import pytest

from simfmri.handlers import AbstractHandler, list_handlers, get_handler
from simfmri.handlers.base import MetaHandler, requires_field
from simfmri.simulation import SimData


class DummyHandler(AbstractHandler):
    """A Dummy Handler"""

    name = "dummy"

    def _handle(self, sim):
        pass


def test_handler_registration():
    """Test handlers registration"""
    assert "dummy" in list_handlers()
    assert "dummy" in MetaHandler.registry
    assert MetaHandler.registry["dummy"] == get_handler("dummy")


def test_handler_chaining():
    """Test handler chaining."""

    class A(AbstractHandler):
        def _handle(self, sim):
            pass

    class B(AbstractHandler):
        def _handle(self, sim):
            pass

    class C(AbstractHandler):
        def _handle(self, sim):
            pass

    a, b, c = A(), B(), C()
    chain = a >> b
    chain_r = b << a
    assert chain_r == chain
    assert chain._handlers == [a, b]

    chain2 = chain >> c
    assert chain2._handlers == [a, b, c]

    assert (a << b >> c) == (b >> a >> c)


def test_requires_field():
    """Test the requires field decorator"""

    @requires_field("custom_field")
    class A(AbstractHandler):
        def _handle(self, sim):
            sim.custom_field += 1

    @requires_field("custom_field", lambda sim: 3)
    class B(AbstractHandler):
        def _handle(self, sim):
            sim.custom_field += 1

    sim = SimData(shape=(48, 48, 32), fov=0.001, sim_time=12, sim_tr=1.0)

    with pytest.raises(ValueError):
        A()(sim)

    sim.custom_field = 0
    A()(sim)
    assert sim.custom_field == 1
    B()(sim)
    assert sim.custom_field == 2

    delattr(sim, "custom_field")
    B()(sim)
    assert sim.custom_field == 4
