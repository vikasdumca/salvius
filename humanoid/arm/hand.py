from marshmallow import Serializer, fields
from humanoid.joints import CompliantJoint, CompliantJointSerializer


class Finger(CompliantJoint):

    def __init__(self, uuid=None, hand_id=None):
        super(Finger, self).__init__()

        self.parent_id = hand_id
        self.id = uuid


class Hand(object):

    def __init__(self):
        self._fingers = []
        self._thumb = None

        self.parent_id = None

    def add_finger(self):
        """
        Adds a finger to the hand.
        Sets a unique id to reference the listed index of the object.
        """
        uuid = 0
        if self._fingers:
            uuid = max(finger.id for finger in self._fingers) + 1

        finger = Finger(uuid, self.parent_id)
        self._fingers.append(finger)

    def set_parent_id(self, uuid):
        self.parent_id = uuid

    def set_thumb(self, thumb):
        """
        Takes a finger object as a parameter.
        """
        self._thumb = thumb

    @property
    def fingers(self):
        return self._fingers

    @property
    def thumb(self):
        return self._thumb

    def close(self):
        """
        Closes all of the hands fingers to make a fist shape.
        """
        for finger in self._fingers:
            finger.move(100)
        self._thumb.move(100)


class FingerSerializer(CompliantJointSerializer):
    id = fields.UUID()
    position = fields.Integer()

    def get_url(self, obj):
        url = "/api/robot/body/arms/" + str(obj.parent_id) + "/hand"

        # Only fingers should be created with an id
        if obj.id is not None:
            url += "/fingers/" + str(obj.id)
        else:
            url += "/thumb"

        return url


class FingersSerializer(Serializer):
    fingers = fields.Nested(FingerSerializer, many=True)


class HandSerializer(Serializer):
    fingers = fields.Nested(FingerSerializer, many=True)
    thumb = fields.Nested(FingerSerializer)
