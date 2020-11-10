import json
import datetime
from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class BaseSerializer(ABC):

    @abstractmethod
    def dumps(self, obj):
        pass

    @abstractmethod
    def loads(self, obj):
        pass

    @abstractmethod
    def deserialize(self, obj):
        pass


class SerializerFactory:
    @classmethod
    def get_serializer(cls):
        if not hasattr(cls, "serializer") or cls.serializer is None:
            cls.serializer = Serializer()
        return cls.serializer

    @classmethod
    def set_serializer(cls, serializer):
        cls.serializer = serializer


class Serializer(BaseSerializer):

    def dumps(self, obj):
        """Converts List to Json String"""
        if isinstance(obj, list):
            return json.dumps(obj, default=lambda x: x.__dict__, cls=Serializer.CustomEncoder, sort_keys=True,
                              indent=4)

        """Converts to Json String"""
        if isinstance(obj, dict):
            return json.dumps(obj, cls=Serializer.CustomEncoder, sort_keys=True, indent=4)

        return json.dumps(obj.__dict__, cls=Serializer.CustomEncoder, sort_keys=True, indent=4).encode()

    def loads(self, obj):
        return json.loads(obj)

    def deserialize(self, obj):
        return self.loads(self.dumps(obj=obj))

    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float("{:.2f}".format(obj))

            if isinstance(obj, UUID):
                return str(obj)

            if isinstance(obj, datetime.datetime):
                return obj.isoformat()

            return json.JSONEncoder.default(self, obj)


class JsonSerializable(object):
    def to_json(self):
        return SerializerFactory.get_serializer().deserialize(obj=self)
