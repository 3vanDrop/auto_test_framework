from framework.can.factory import CANMessageFactory
from framework.can.message import StandardCANMessage, ExtendedCANMessage


def test_factory_creates_standard_and_extended():
    """CANMessageFactory should return the correct subclass."""
    std = CANMessageFactory.create(0x100, b'\x01\x02', is_extended_id=False)
    ext = CANMessageFactory.create(0x1ABCDE, b'\x03\x04', is_extended_id=True)

    assert isinstance(std, StandardCANMessage)
    assert std.arbitration_id == 0x100
    assert std.data == b'\x01\x02'
    assert std.is_extended_id is False

    assert isinstance(ext, ExtendedCANMessage)
    assert ext.arbitration_id == 0x1ABCDE
    assert ext.data == b'\x03\x04'
    assert ext.is_extended_id is True
