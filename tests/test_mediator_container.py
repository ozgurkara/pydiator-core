from pydiator_core.mediatr_container import MediatrContainer
from pydiator_core.interfaces import BaseRequest, BaseNotification
from tests.base_test_case import BaseTestCase, TestPipeline, TestRequest, TestResponse, TestHandler, TestNotification, \
    TestNotificationHandler


class TestMediatrContainer(BaseTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_default_values_when_create_instance(self):
        # Given

        # When
        container = MediatrContainer()

        # Then
        assert container.get_requests() == {}
        assert container.get_notifications() == {}
        assert container.get_pipelines() == []
        assert container._MediatrContainer__base_notification_get_class_method_name == BaseNotification.get_class_name.__name__
        assert container._MediatrContainer__base_notification_get_class_method_name == BaseRequest.get_class_name.__name__

    def test_register_pipeline(self):
        # Given
        container = MediatrContainer()
        response = TestResponse(success=True)

        # When
        container.register_pipeline(TestPipeline(response))

        # Then
        assert container.get_requests() == {}
        assert container.get_notifications() == {}
        assert len(container.get_pipelines()) == 1

    def test_get_pipelines(self):
        # Given
        response = TestResponse(success=True)
        container = MediatrContainer()
        pipeline = TestPipeline(response)

        # When
        container.register_pipeline(pipeline)
        response = container.get_pipelines()

        # Then
        assert container.get_requests() == {}
        assert container.get_notifications() == {}
        assert len(response) == 1
        assert response[0] is pipeline

    def test_register_notification_when_added_notification(self):
        # Given
        container = MediatrContainer()

        # When
        container.register_notification(TestNotification, [TestNotificationHandler()])

        # Then
        assert container.get_requests() == {}
        assert container.get_pipelines() == []
        assert len(container.get_notifications()) == 1

    def test_register_notification_when_notification__is_not_instance_of_base_notification(self):
        # Given
        container = MediatrContainer()

        # When
        container.register_notification(MediatrContainer, [TestNotificationHandler()])
        response = container.get_notifications()

        # Then
        assert container.get_requests() == {}
        assert container.get_pipelines() == []
        assert len(response) == 0

    def test_get_notifications(self):
        # Given
        container = MediatrContainer()
        handlers = [TestNotificationHandler()]

        # When
        container.register_notification(TestNotification, handlers)
        response = container.get_notifications()

        # Then
        assert container.get_requests() == {}
        assert container.get_pipelines() == []
        assert len(response) == 1
        assert response[TestNotification.get_class_name()] is not None
        assert response[TestNotification.get_class_name()] == handlers

    def test_register_request(self):
        # Given
        request = TestRequest()
        handler = TestHandler()
        container = MediatrContainer()

        # When
        container.register_request(req=TestRequest, handler=handler)

        # Then
        assert container.get_notifications() == {}
        assert len(container.get_requests()) == 1
        assert container.get_requests()[TestRequest.get_class_name()] is not None
        assert container.get_requests()[TestRequest.get_class_name()] == handler

    def test_register_request_return_when_request_is_not_instance_of_base_request(self):
        # Given
        handler = TestHandler()
        container = MediatrContainer()

        # When
        container.register_request(req=TestResponse, handler=handler)

        # Then
        assert len(container.get_requests()) == 0

    def test_register_request_return_when_handler_is_not_instance_of_base_handler(self):
        # Given
        container = MediatrContainer()

        # When
        container.register_request(req=TestRequest, handler={})

        # Then
        assert len(container.get_requests()) == 0

    def test_prepare_pipes_when_pipelines_length_is_equal_1(self):
        # Given
        response = TestResponse(success=True)
        container = MediatrContainer()
        test_pipeline = TestPipeline(response)

        # When
        container.prepare_pipes(test_pipeline)

        # Then
        assert len(container.get_pipelines()) == 1
        assert test_pipeline.has_next() is False

    def test_prepare_pipes_when_pipelines_length_is_greater_than_1(self):
        # Given
        response = TestResponse(success=True)
        test_pipeline = TestPipeline(response)
        test_default_pipeline = TestPipeline(response)

        container = MediatrContainer()
        container.register_pipeline(test_pipeline)

        # When
        container.prepare_pipes(test_default_pipeline)

        # Then
        assert len(container.get_pipelines()) == 2
        assert test_pipeline.has_next()
        assert test_default_pipeline.has_next() is False
