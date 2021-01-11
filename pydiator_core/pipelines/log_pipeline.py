from typing import List
from pydiator_core.interfaces import BaseRequest, BasePipeline
from pydiator_core.logger import LoggerFactory
from pydiator_core.serializer import SerializerFactory


class LogPipeline(BasePipeline):
    def __init__(self):
        self.serializer = SerializerFactory.get_serializer()
        self.logger = LoggerFactory.get_logger()

    async def handle(self, req: BaseRequest, **kwargs) -> object:

        if self.next() is None:
            raise Exception("pydiator_log_pipeline_has_no_next_pipeline")

        next_handle = getattr(self.next(), "handle", None)
        if next_handle is None or not callable(next_handle):
            raise Exception("handle_function_of_next_pipeline_is_not_valid_for_log_pipeline")

        response = await next_handle(req=req, **kwargs)

        if hasattr(response, "__dict__") or isinstance(response, List):
            _response = self.serializer.deserialize(response)
        else:
            _response = str(response)

        log_obj = {
            "req": self.serializer.deserialize(req),
            "res": _response
        }

        req_type_name = req.get_class_name()
        self.logger.log(source=self.__class__.__name__, message=req_type_name, data=log_obj)

        return response
