from framework.can.message import CANMessage


def test_can_message_to_bytes():
    """CANMessage.to_bytes() must return exactly its data payload."""
    payload = b'\xAA\xBB\xCC'
    msg = CANMessage(0x200, payload)

    assert msg.to_bytes() == payload
