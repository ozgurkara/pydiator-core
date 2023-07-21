import datetime
import uuid
from decimal import Decimal
from typing import List
from uuid import UUID

from pydiator_core.interfaces import BaseResponse
from pydiator_core.serializer import Serializer
from tests.base_test_case import BaseTestCase, TestResponse


class TestSerializer(BaseTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dumps_when_type_is_list(self):
        # Given
        serializer = Serializer()
        obj = [{"name": "1"}, {"name": "2"}]

        # When
        response = serializer.dumps(obj)

        # Then
        assert response is not None
        assert len(serializer.loads(response)) == 2

    def test_dumps_when_type_is_dict(self):
        # Given
        serializer = Serializer()
        obj = {
            "name": 1
        }

        # When
        response = serializer.dumps(obj)

        # Then
        assert response is not None
        assert len(serializer.loads(response)) == 1

    def test_dumps(self):
        # Given
        serializer = Serializer()
        obj = TestResponse(success=True)

        # When
        response = serializer.dumps(obj)

        # Then
        assert response is not None
        assert len(serializer.loads(response)) == 1

    def test_loads(self):
        # Given
        serializer = Serializer()
        obj = TestResponse(success=True)
        dump = serializer.dumps(obj)

        # When
        response = serializer.loads(dump)

        # Then
        assert response is not None
        assert response["success"]

    def test_deserialize(self):
        # Given
        class TestItem(BaseResponse):
            def __init__(self, id: int, title: str):
                self.id = id,
                self.title = title

        class TestMixResponse(BaseResponse):
            def __init__(self, text: str, success: bool, dec: Decimal, uid: UUID, dt: datetime.datetime,
                         date: datetime.date,
                         item: TestItem, items: List[TestItem]):
                self.text = text
                self.success = success
                self.dec = dec
                self.uid = uid
                self.dt = dt
                self.date = date
                self.item = item
                self.items = items

        time = datetime.datetime.now()
        date = datetime.datetime.date(time)
        uid = uuid.uuid4()
        item = TestItem(3, "title3")
        items = [TestItem(1, "title1"), TestItem(2, "title2")]
        mix_response = TestMixResponse(text="bla bla",
                                       success=True,
                                       dec=Decimal.from_float(1.123),
                                       uid=uid,
                                       dt=time,
                                       date=date,
                                       item=item,
                                       items=items)

        # When
        response = mix_response.to_json()

        # Then
        assert response is not None
        assert mix_response.text == response["text"]
        assert mix_response.success == response["success"]
        assert 1.12 == response["dec"]
        assert str(mix_response.uid) == response["uid"]
        assert time.isoformat() == str(response["dt"])
        assert datetime.datetime.date(time).isoformat() == str(response["date"])
        assert item.title == response["item"]["title"]
        assert len(items) == len(response["items"])
