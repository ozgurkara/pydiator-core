import inspect

from pydiator_core.interfaces import BaseRequest, BasePipeline
from pydiator_core.mediatr_container import BaseMediatrContainer


class DefaultPipeline(BasePipeline):
    def __init__(self, mediatr_container: BaseMediatrContainer):
        self.mediatr_container = mediatr_container

    async def handle(self, req: BaseRequest, **kwargs) -> object:
        req_type_name = req.get_class_name()
        handler = self.mediatr_container.get_requests().get(req_type_name, None)
        if handler is None:
            raise Exception(f"handler_not_found_for_request_:{req_type_name}")

        handle_func = getattr(handler, "handle", None)
        if not callable(handle_func):
            raise Exception("handle_function_has_not_found_in_handler")

        is_async = inspect.iscoroutinefunction(handler.handle)
        if not is_async:
            return handler.handle(req)

        return await handler.handle(req)
