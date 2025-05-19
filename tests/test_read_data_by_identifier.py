import pytest
from framework.utils.can_interface import CANInterface
from framework.uds.service import UDSService


@pytest.fixture
def can_iface():
    # Use a virtual CAN interface for tests
    return CANInterface(channel='vcan0', bustype='socketcan', bitrate=500000)


def test_read_did_0xF190(can_iface):
    uds = UDSService(can_iface, tx_id=0x7E0, rx_id=0x7E8)
    data = uds.read_data_by_identifier(0xF190, timeout=1.5)
    assert isinstance(data, bytes)
    assert len(data) >= 1
