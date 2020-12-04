from unittest import mock
from unittest.mock import MagicMock

from pydiator_core.interfaces import BaseNotification
from pydiator_core.logger import LoggerFactory, BaseLogger
from pydiator_core.mediatr import Mediatr
from pydiator_core.serializer import SerializerFactory, BaseSerializer
from tests.base_test_case import BaseTestCase, TestRequest, TestResponse, FakeMediatrContainer, TestNotification


class TestMediatrContainer(BaseTestCase):

    def setUp(self):
        SerializerFactory.set_serializer(None)
        LoggerFactory.set_logger(None)

    def tearDown(self):
        pass

    def test_read_default_values_when_create_instance(self):
        # Given

        # When
        mediatr = Mediatr()

        # Then
        assert mediatr.is_ready is False

    def test_ready_when_is_ready(self):
        # Given
        mediatr = Mediatr()
        mediatr.is_ready = True

        # When
        mediatr.ready(container=None)

        # Then
        assert mediatr.is_ready

    def test_ready_when_is_not_ready(self):
        # Given
        container = FakeMediatrContainer()
        mediatr = Mediatr()

        # When
        mediatr.ready(container=container)

        # Then
        assert mediatr.is_ready
        assert len(container.get_pipelines()) == 1

    def test_ready_when_container_is_none(self):
        # Given
        mediatr = Mediatr()

        # When
        with self.assertRaises(Exception) as context:
            mediatr.ready(container=None)

        # Then
        assert mediatr.is_ready is False
        assert 'mediatr_container_is_none' == context.exception.args[0]

    def test_ready_when_serializer_is_not_none(self):
        # Given
        container = FakeMediatrContainer()
        mediatr = Mediatr()

        # When
        mediatr.ready(container=container, serializer={})

        # Then
        assert mediatr.is_ready is True
        assert SerializerFactory.get_serializer() == {}

    def test_ready_when_serializer_is_none(self):
        # Given
        mediatr_container = FakeMediatrContainer()
        mediatr = Mediatr()

        # When
        mediatr.ready(container=mediatr_container)

        # Then
        assert mediatr.is_ready is True
        assert isinstance(SerializerFactory.get_serializer(), BaseSerializer)

    def test_ready_when_container_and_serializer_set(self):
        # Given
        container = FakeMediatrContainer()
        mediatr = Mediatr()

        # When
        mediatr.ready(container=container, serializer={})

        # Then
        assert mediatr.is_ready is True
        assert not isinstance(SerializerFactory.get_serializer(), BaseSerializer)
        assert SerializerFactory.get_serializer() == {}
        assert len(container.get_pipelines()) == 1

    def test_ready_when_container_and_logger_set(self):
        # Given
        container = FakeMediatrContainer()
        mediatr = Mediatr()

        # When
        mediatr.ready(container=container, logger={})

        # Then
        assert mediatr.is_ready is True
        assert not isinstance(LoggerFactory.get_logger(), BaseLogger)
        assert LoggerFactory.get_logger() == {}
        assert len(container.get_pipelines()) == 1

    def test_ready_when_logger_is_none(self):
        # Given
        container = FakeMediatrContainer()
        mediatr = Mediatr()

        # When
        mediatr.ready(container=container)

        # Then
        assert mediatr.is_ready is True
        assert isinstance(LoggerFactory.get_logger(), BaseLogger)

    def test_send_raise_exception_when_container_is_none(self):
        # Given
        mediatr = Mediatr()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert 'mediatr_container_is_none' == context.exception.args[0]

    def test_send_raise_exception_when_container_pipelines_is_empty(self):
        # Given
        container = MagicMock()
        container.get_pipelines.return_value = []
        mediatr = Mediatr()
        mediatr.ready(container=container)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert 'mediatr_container_has_not_contain_any_pipeline' == context.exception.args[0]

    @mock.patch("pydiator_core.mediatr.DefaultPipeline")
    def test_send_return_default_pipeline_result_when_container_pipelines_is_empty(self, mock_default_pipeline):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        mock_default_pipeline.return_value.handle = next_handle
        container = FakeMediatrContainer()
        mediatr = Mediatr()
        mediatr.ready(container)

        # When
        response = self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert response is next_response
        assert response.success

    def test_publish_when_handlers_is_empty(self):
        # Given
        container = FakeMediatrContainer()
        mediatr = Mediatr()
        container.register_notification(TestNotification(), [])
        mediatr.ready(container)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.publish(BaseNotification()))

        # Then
        assert 'mediatr_container_has_not_contain_any_notification_handler_for:BaseNotification' == \
               context.exception.args[0]

    def test_publish_when_handlers_exist(self):
        # Given
        async def next_handle(notification):
            pass

        mock_notification_handler = mock.MagicMock()
        mock_notification_handler.handle.side_effect = next_handle

        container = FakeMediatrContainer()
        container.register_notification(TestNotification(), [mock_notification_handler])

        mediatr = Mediatr()
        mediatr.ready(container)

        # When
        self.async_loop(mediatr.publish(TestNotification()))

        # Then
        assert mock_notification_handler.handle.called
        assert mock_notification_handler.handle.call_count == 1

    def test_publish_when_handle_has_exception(self):
        # Given
        async def next_handle(notification):
            raise Exception("")

        mock_notification_handler = mock.MagicMock()
        mock_notification_handler.handle.side_effect = next_handle

        container = FakeMediatrContainer()
        container.register_notification(TestNotification(), [mock_notification_handler])

        mediatr = Mediatr()
        mediatr.ready(container)

        # When
        self.async_loop(mediatr.publish(notification=TestNotification()))

        # Then
        assert mock_notification_handler.handle.called
        assert mock_notification_handler.handle.call_count == 1

    def test_publish_when_handle_has_exception_and_throw_exception(self):
        # Given
        async def next_handle(notification):
            raise Exception("test_exception")

        mock_notification_handler = mock.MagicMock()
        mock_notification_handler.handle.side_effect = next_handle

        container = FakeMediatrContainer()
        container.register_notification(TestNotification(), [mock_notification_handler])

        mediatr = Mediatr()
        mediatr.ready(container)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.publish(notification=TestNotification(), throw_exception=True))

        # Then
        assert mock_notification_handler.handle.called
        assert mock_notification_handler.handle.call_count == 1
        assert 'test_exception' == context.exception.args[0]
