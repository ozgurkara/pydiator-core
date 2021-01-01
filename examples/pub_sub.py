import asyncio

from pydiator_core.interfaces import BaseNotificationHandler, BaseNotification


# publisher object
class SamplePublisherRequest(BaseNotification):
    def __init__(self, id: int):
        self.id = id


# subscriber 1
class Sample1Subscriber(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SamplePublisherRequest):
        print("Sample 1 Subscriber handled:id", notification.id)


# subscriber 2
class Sample2Subscriber(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SamplePublisherRequest):
        print("Sample 2 Subscriber handled:id", notification.id)


# subscriber 3
class Sample3Subscriber(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: SamplePublisherRequest):
        print("Sample 3 Subscriber handled:id", notification.id)


from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer


def set_up_pydiator():
    container = MediatrContainer()
    # Sample1Subscriber,Sample2Subscriber,Sample3Subscriber are triggered for every SamplePublisherRequest
    container.register_notification(SamplePublisherRequest, [Sample1Subscriber(), Sample2Subscriber(),
                                                             Sample3Subscriber()])
    pydiator.ready(container=container)


if __name__ == "__main__":
    set_up_pydiator()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pydiator.publish(SamplePublisherRequest(id=1)))
    loop.close()
