from pydiator_core.serializer import BaseSerializer, SerializerFactory
from tests.base_test_case import BaseTestCase, TestResponse


class TestSerializer(BaseTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_serializer_when_set_serializer(self):
        # Given
        class TestSerializerObj(BaseSerializer):

            def dumps(self, obj):
                return ""

            def loads(self, obj):
                return "test"

            def deserialize(self, obj):
                return self.loads(self.dumps(obj))

        test_serializer = TestSerializerObj()
        SerializerFactory.set_serializer(serializer=test_serializer)

        test_response = TestResponse(True)

        # When
        response = test_response.to_json()

        # Then
        assert response == "test"
        assert test_serializer == SerializerFactory.get_serializer()
