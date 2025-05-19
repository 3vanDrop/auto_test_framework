import can
from framework.can.factory import CANMessageFactory
from scapy.layers.can import CAN
from scapy.layers.iso15765 import ISOTP_Cmd


class CANInterface:
    """Abstraction over python-can + Scapy ISOTP."""
    def __init__(self, channel='vcan0', bustype='socketcan', bitrate=500000):
        self.bus = can.interface.Bus(channel=channel,
                                     bustype=bustype,
                                     bitrate=bitrate)

    def send(self, frame):
        """Send a CANMessage object."""
        msg = can.Message(
            arbitration_id=frame.arbitration_id,
            is_extended_id=frame.is_extended_id,
            data=frame.data,
            timestamp=frame.timestamp.timestamp()
        )
        self.bus.send(msg)

    def recv(self, timeout: float = 1.0):
        """Receive a raw CAN message and wrap it in a CANMessage."""
        raw = self.bus.recv(timeout)
        if raw is None:
            return None
        return CANMessageFactory.create(raw.arbitration_id,
                                        raw.data,
                                        raw.is_extended_id)

    def send_isotp(self, sid: int, payload: bytes, tx_id: int, rx_id: int):
        """
        Build and send an ISO-TP UDS packet via Scapy.
        sid: UDS service ID (e.g. 0x22)
        payload: UDS payload (e.g. DID bytes)
        tx_id: CAN arbitration ID to transmit
        rx_id: CAN arbitration ID to receive
        """
        iso = ISOTP_Cmd(source_address=tx_id,
                        target_address=rx_id,
                        data=bytes([sid]) + payload)
        can_pkt = CAN(id=tx_id, data=bytes(iso))
        self.bus.send(can.Message(
            arbitration_id=tx_id,
            is_extended_id=False,
            data=can_pkt.data
        ))
