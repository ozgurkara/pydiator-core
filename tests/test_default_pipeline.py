from unittest import mock

from pydiator_core.default_pipeline import DefaultPipeline
from pydiator_core.interfaces import BaseResponse
from pydiator_core.mediatr_container import MediatrContainer
from tests.base_test_case import BaseTestCase, TestRequest, TestHandler, TestSyncHandler


class TestDefaultPipeline(BaseTestCase):
    def setUp(self):
        pass

    def test_handle_return_exception_when_handler_is_not(self):
        # Given
        pipeline = DefaultPipeline(MediatrContainer())

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(pipeline.handle(req=TestRequest()))

        # Then
        assert context.exception.args[0] == f'handler_not_found_for_request_:{type(TestRequest()).__name__}'

    def test_handle_return_exception_when_handler_is_not_callable(self):
        # Given
        mock_container = mock.MagicMock()
        mock_container.get_requests.return_value.get.return_value = {}
        self.pipeline = DefaultPipeline(mock_container)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(self.pipeline.handle(req=TestRequest()))

        # Then
        assert 'handle_function_has_not_found_in_handler' == context.exception.args[0]

    def test_handle_return_handle_response(self):
        # Given
        container = MediatrContainer()
        container.register_request(TestRequest, TestHandler())
        self.pipeline = DefaultPipeline(container)

        # When
        response = self.async_loop(self.pipeline.handle(req=TestRequest()))

        # Then
        assert isinstance(response, BaseResponse)

    def test_handle_return_handle_response_when_handle_is_sync(self):
        # Given
        container = MediatrContainer()
        container.register_request(TestRequest, TestSyncHandler())
        self.pipeline = DefaultPipeline(container)

        # When
        response = self.async_loop(self.pipeline.handle(req=TestRequest()))

        # Then
        assert isinstance(response, BaseResponse)
