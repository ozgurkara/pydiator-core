import asyncio

from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from pydiator_core.pipelines.log_pipeline import LogPipeline


class GetByIdRequest(BaseRequest):
    def __init__(self, id: int):
        self.id = id


class GetByIdResponse(BaseResponse):
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title


class GetByIdHandler(BaseHandler):
    async def handle(self, req: GetByIdRequest):
        # related codes are here such as business
        return GetByIdResponse(id=req.id, title="hello pydiatr")


from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer


def set_up_pydiator():
    container = MediatrContainer()
    container.register_request(GetByIdRequest, GetByIdHandler())
    container.register_pipeline(LogPipeline())
    pydiator.ready(container=container)


if __name__ == "__main__":
    set_up_pydiator()
    loop = asyncio.new_event_loop()
    response: GetByIdResponse = loop.run_until_complete(pydiator.send(GetByIdRequest(id=1)))
    loop.close()
    print(response.to_json())
