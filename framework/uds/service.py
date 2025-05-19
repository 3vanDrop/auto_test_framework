from scapy.layers.iso15765 import ISOTP_Rsp
from framework.utils.can_interface import CANInterface


class UDSService:
    """High-level UDS service API over ISO-TP / CAN."""
    def __init__(self, can_if: CANInterface, tx_id: int, rx_id: int):
        self.can_if = can_if
        self.tx_id = tx_id
        self.rx_id = rx_id

    def read_data_by_identifier(self, did: int, timeout: float = 1.0) -> bytes:
        """
        Send a ReadDataByIdentifier (0x22) request and wait for a 0x62 response.
        Returns the raw DID data payload.
        """
        # Build & send request
        payload = did.to_bytes(2, byteorder='big')
        self.can_if.send_isotp(0x22, payload, tx_id=self.tx_id, rx_id=self.rx_id)

        # Receive response
        resp = self.can_if.recv(timeout)
        if resp is None:
            raise TimeoutError("No response received for UDS ReadDataByIdentifier")

        # Parse ISO-TP response
        iso = ISOTP_Rsp(bytes([resp.arbitration_id & 0xFF]) + resp.data)
        if iso.service != 0x62:
            raise ValueError(f"Unexpected service ID: 0x{iso.service:X}")

        return iso.data
