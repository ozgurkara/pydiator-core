from unittest import mock
from unittest.mock import MagicMock

from pydiator_core.pipelines.log_pipeline import LogPipeline
from pydiator_core.serializer import SerializerFactory
from tests.base_test_case import BaseTestCase, TestRequest, TestResponse


class TestLogPipeline(BaseTestCase):
    def setUp(self):
        SerializerFactory.set_serializer(None)

    def tearDown(self):
        pass

    def test_handle_return_exception_when_next_is_none(self):
        # Given
        log_pipeline = LogPipeline()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert context.exception.args[0] == 'pydiator_log_pipeline_has_no_next_pipeline'

    def test_handle_return_exception_when_next_handle_is_none(self):
        # Given
        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = None

        log_pipeline = LogPipeline()
        log_pipeline.set_next(mock_test_pipeline)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert context.exception.args[0] == 'handle_function_of_next_pipeline_is_not_valid_for_log_pipeline'

    def test_handle_when_response_is_str(self):
        # Given
        next_response_text = "next_response"

        async def next_handle(req):
            return next_response_text

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        log_pipeline = LogPipeline()
        log_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert response is not None
        assert response == next_response_text

    @mock.patch("pydiator_core.pipelines.log_pipeline.LoggerFactory")
    @mock.patch("pydiator_core.pipelines.log_pipeline.SerializerFactory")
    def test_handle_when_response_is_instance_of_dict(self, mock_serializer_factory, mock_logger_factory):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        log_pipeline = LogPipeline()
        log_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert response is not None
        assert response == next_response
        assert mock_serializer_factory.get_serializer.called
        assert mock_serializer_factory.get_serializer.return_value.deserialize.called
        assert mock_serializer_factory.get_serializer.return_value.deserialize.call_count == 2

    @mock.patch("pydiator_core.pipelines.log_pipeline.LoggerFactory")
    @mock.patch("pydiator_core.pipelines.log_pipeline.SerializerFactory")
    def test_handle_when_response_type_is_list(self, mock_serializer_factory, mock_logger_factory):
        # Given
        next_response = [TestResponse(success=True)]

        async def next_handle(req):
            return next_response

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        log_pipeline = LogPipeline()
        log_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert response is not None
        assert response == next_response
        assert len(response) == 1
        assert mock_serializer_factory.get_serializer.called
        assert mock_serializer_factory.get_serializer.return_value.deserialize.called
        assert mock_serializer_factory.get_serializer.return_value.deserialize.call_count == 2
        assert mock_logger_factory.get_logger.called
        assert mock_logger_factory.get_logger.return_value.log.called
        assert mock_logger_factory.get_logger.return_value.log.call_count == 1

    @mock.patch("pydiator_core.pipelines.log_pipeline.LoggerFactory")
    def test_handle_log_when_response_type_is_list(self, mock_logger_factory):
        # Given
        next_response = [TestResponse(success=True)]

        async def next_handle(req):
            return next_response

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        log_pipeline = LogPipeline()
        log_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert response is not None
        assert response == next_response
        assert len(response) == 1
        assert mock_logger_factory.get_logger.called
        assert mock_logger_factory.get_logger.return_value.log.called
        assert mock_logger_factory.get_logger.return_value.log.call_count == 1
        mock_logger_factory.get_logger.return_value. \
            log.assert_called_once_with(source="LogPipeline",
                                        message="TestRequest",
                                        data={'req': {}, 'res': [{'success': True}]})
