import asyncio
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as asynchronous")


def pytest_pyfunc_call(pyfuncitem):
    if pyfuncitem.get_closest_marker("asyncio"):
        loop = pyfuncitem.funcargs.get(
            "event_loop", asyncio.new_event_loop()
        )
        asyncio.set_event_loop(loop)
        loop.run_until_complete(pyfuncitem.obj(**pyfuncitem.funcargs))
        return True
    return None
