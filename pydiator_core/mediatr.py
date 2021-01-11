from pydiator_core.interfaces import BaseRequest, BaseNotification, BaseMediatr, BaseMediatrContainer
from pydiator_core.default_pipeline import DefaultPipeline
from pydiator_core.logger import LoggerFactory, BaseLogger
from pydiator_core.serializer import BaseSerializer, SerializerFactory


class Mediatr(BaseMediatr):

    def __init__(self):
        self.__container = None
        self.is_ready = False

    def ready(self, container: BaseMediatrContainer, serializer: BaseSerializer = None, logger: BaseLogger = None):
        if self.is_ready:
            return

        if container is None:
            raise Exception("mediatr_container_is_none")

        self.__container = container
        self.__container.prepare_pipes(DefaultPipeline(self.__container))

        if serializer is not None:
            SerializerFactory.set_serializer(serializer)

        if logger is not None:
            LoggerFactory.set_logger(logger)

        self.is_ready = True

    async def send(self, req: BaseRequest, **kwargs) -> object:
        if self.__container is None:
            raise Exception("mediatr_container_is_none")

        pipelines = self.__container.get_pipelines()
        if len(pipelines) == 0:
            raise Exception("mediatr_container_has_not_contain_any_pipeline")

        return await pipelines[0].handle(req=req, **kwargs)

    async def publish(self, notification: BaseNotification, throw_exception: bool = False):
        notification_type_name = notification.get_class_name()
        notifications_obj = self.__container.get_notifications()
        if notification_type_name not in notifications_obj:
            raise Exception(f"mediatr_container_has_not_contain_any_notification_handler_for:{notification_type_name}")

        handlers = notifications_obj[notification_type_name]
        for h in handlers:
            if not throw_exception:
                try:
                    await h.handle(notification)
                except Exception as e:
                    print("exception_when_notification_handle:", str(e))
            else:
                await h.handle(notification)


pydiator = Mediatr()
