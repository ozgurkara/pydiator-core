from typing import List
from pydiator_core.interfaces import BaseRequest, BasePipeline
from pydiator_core.logger import LoggerFactory
from pydiator_core.serializer import SerializerFactory


class LogPipeline(BasePipeline):
    def __init__(self):
        self.serializer = SerializerFactory.get_serializer()
        self.logger = LoggerFactory.get_logger()

    async def handle(self, req: BaseRequest) -> object:
        req_type_name = req.get_class_name()

        if self.next() is None:
            raise Exception("pydiator_log_pipeline_has_no_next_pipeline")

        response = await self.next().handle(req)

        if hasattr(response, "__dict__") or isinstance(response, List):
            _response = self.serializer.deserialize(response)
        else:
            _response = str(response)

        log_obj = {
            "req": self.serializer.deserialize(req),
            "res": _response
        }

        self.logger.log(source=self.__class__.__name__, message=req_type_name, data=log_obj)

        return response
