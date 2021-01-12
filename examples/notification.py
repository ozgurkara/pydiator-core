import asyncio

from pydiator_core.interfaces import BaseNotificationHandler, BaseNotification


# notification object
class SampleNotification(BaseNotification):
    def __init__(self, id: int):
        self.id = id


# subscriber 1
class Sample1Subscriber(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SampleNotification):
        print("Sample 1 Subscriber handled:id", notification.id)


# subscriber 2
class Sample2Subscriber(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SampleNotification):
        print("Sample 2 Subscriber handled:id", notification.id)


# subscriber 3
class Sample3Subscriber(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SampleNotification):
        print("Sample 3 Subscriber handled:id", notification.id)


from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer


def set_up_pydiator():
    container = MediatrContainer()
    # Sample1Subscriber,Sample2Subscriber,Sample3Subscriber are triggered for every SampleNotification
    container.register_notification(SampleNotification, [Sample1Subscriber(), Sample2Subscriber(),
                                                         Sample3Subscriber()])
    pydiator.ready(container=container)


if __name__ == "__main__":
    set_up_pydiator()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pydiator.publish(SampleNotification(id=1)))
    loop.close()
