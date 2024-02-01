# pylint: skip-file
import asyncio

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


async def raise_exception():
    await asyncio.sleep(1)
    raise Exception("Some error")


async def init_foo(value: str):
    await raise_exception()
    yield {"bar": value}


class BaseContainer(containers.DeclarativeContainer):
    foo = providers.Resource(init_foo, "some-value")


class WorkerContainer(containers.DeclarativeContainer):
    base = providers.Container(BaseContainer)


@inject
async def main(
    container=Provide[WorkerContainer], foo=Provide[WorkerContainer.base.foo]
):
    await container.init_resources()

    print("foo", foo)

    for _ in range(5):
        print("working and sleeping...")
        await asyncio.sleep(1)

    await container.shutdown_resources()


if __name__ == "__main__":
    worker_container = WorkerContainer()
    worker_container.wire(modules=[__name__])
    asyncio.run(main())
