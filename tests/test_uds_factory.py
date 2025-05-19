import pytest
from framework.can.message import CANMessage
from framework.uds.service import UDSService


# A very minimal dummy CAN‐interface to drive UDSService without real bus
class DummyInterface:
    def __init__(self, to_recv):
        # to_recv: either a CANMessage or None
        self.to_recv = to_recv
        self.sent = []

    def send_isotp(self, sid, payload, tx_id, rx_id):
        # record the parameters of every request
        self.sent.append((sid, payload, tx_id, rx_id))

    def recv(self, timeout):
        # simulate bus.recv()
        return self.to_recv


@pytest.fixture
def uds_factory():
    """Helper to create a UDSService backed by a DummyInterface."""
    def _make(to_recv):
        di = DummyInterface(to_recv)
        # tx_id=0x700, rx_id=0x708 are arbitrary for tests
        return UDSService(di, tx_id=0x700, rx_id=0x708), di
    return _make


def test_uds_service_timeout(uds_factory):
    """If recv() returns None, UDSService should raise TimeoutError."""
    uds, _di = uds_factory(to_recv=None)
    with pytest.raises(TimeoutError):
        uds.read_data_by_identifier(0x1234, timeout=0.01)


def test_uds_service_unexpected_service(uds_factory):
    """
    If the response has a service ID != 0x62, UDSService should raise ValueError.
    We simulate a resp.data that begins with 0x63.
    """
    # Build a dummy CANMessage with "wrong" service 0x63
    wrong_resp = CANMessage(
        arbitration_id=0x708,
        data=bytes([0x63, 0x12, 0x34, 0x00])  # service=0x63, DID=0x1234, no payload
    )
    uds, _di = uds_factory(to_recv=wrong_resp)

    with pytest.raises(ValueError):
        uds.read_data_by_identifier(0x1234, timeout=0.01)


def test_uds_service_success(uds_factory):
    """
    Simulate a correct ReadDataByIdentifier response:
      - service = 0x62
      - DID high, DID low
      - some payload bytes (e.g. 0xDE, 0xAD)
    UDSService should return only the payload (0xDE,0xAD).
    """
    # resp.data = [0x62, 0x12, 0x34, 0xDE, 0xAD]
    good_resp = CANMessage(
        arbitration_id=0x708,
        data=bytes([0x62, 0x12, 0x34, 0xDE, 0xAD])
    )
    uds, di = uds_factory(to_recv=good_resp)

    result = uds.read_data_by_identifier(0x1234, timeout=0.01)
    assert result == bytes([0xDE, 0xAD])

    # also verify that send_isotp was called with correct parameters
    # expect SID=0x22, payload=DID bytes, tx_id=0x700, rx_id=0x708
    assert di.sent == [
        (0x22, (0x1234).to_bytes(2, byteorder='big'), 0x700, 0x708)
    ]
