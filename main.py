# pylint: skip-file
import asyncio

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


async def init_foo():
    raise Exception("Some error")
    print("Foo: init")
    yield {"bar": "foo"}
    print("Foo: shutting down")
    await asyncio.sleep(1)


class Container(containers.DeclarativeContainer):
    foo = providers.Resource(init_foo)


@inject
async def main(foo=Provide[Container.foo], container=Provide[Container]):
    await container.init_resources()
    print(f"foo {foo}")

    for _ in range(5):
        print("working and sleeping...")
        await asyncio.sleep(1)

    await container.shutdown_resources()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    asyncio.run(main())
