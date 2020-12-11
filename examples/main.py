import asyncio

from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from pydiator_core.pipelines.log_pipeline import LogPipeline


class GetSampleByIdRequest(BaseRequest):
    def __init__(self, id: int):
        self.id = id


class GetSampleByIdResponse(BaseResponse):
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title


class GetSampleByIdUseCase(BaseHandler):
    async def handle(self, req: GetSampleByIdRequest):
        # related codes are here such as business
        return GetSampleByIdResponse(id=req.id, title="hello pydiator")


from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer


def set_up_pydiator():
    container = MediatrContainer()
    container.register_request(GetSampleByIdRequest, GetSampleByIdUseCase())
    container.register_pipeline(LogPipeline())
    pydiator.ready(container=container)


if __name__ == "__main__":
    set_up_pydiator()
    loop = asyncio.new_event_loop()
    response: GetSampleByIdResponse = loop.run_until_complete(pydiator.send(GetSampleByIdRequest(id=1)))
    loop.close()
    print(response.to_json())
