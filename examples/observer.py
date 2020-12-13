import asyncio

from pydiator_core.interfaces import BaseNotificationHandler, BaseNotification


# publisher object
class SampleObserverRequest(BaseNotification):
    def __init__(self, id: int):
        self.id = id


# subscriber 1
class Sample1Observer(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SampleObserverRequest):
        print("Sample1Observer:id", notification.id)


# subscriber 2
class Sample2Observer(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SampleObserverRequest):
        print("Sample2Observer:id", notification.id)


# subscriber 3
class Sample3Observer(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SampleObserverRequest):
        print("Sample3Observer:id", notification.id)


from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer


def set_up_pydiator():
    container = MediatrContainer()
    container.register_notification(SampleObserverRequest, [Sample1Observer(), Sample2Observer(),
                                                            Sample3Observer()])
    pydiator.ready(container=container)


if __name__ == "__main__":
    set_up_pydiator()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pydiator.publish(SampleObserverRequest(id=1)))
    loop.close()
