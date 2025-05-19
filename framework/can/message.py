from datetime import datetime


class CANMessage:
    """Base class for a generic CAN message."""
    def __init__(self, arbitration_id: int, data: bytes,
                 is_extended_id: bool = False):
        self.arbitration_id = arbitration_id
        self.data = data
        self.is_extended_id = is_extended_id
        self.timestamp = datetime.now()

    def __repr__(self):
        id_type = "Extended" if self.is_extended_id else "Standard"
        return f"<CANMessage {id_type} ID=0x{self.arbitration_id:X} "\
            "DATA={self.data.hex()}>"

    def to_bytes(self) -> bytes:
        """Return raw data payload."""
        return self.data


class StandardCANMessage(CANMessage):
    """Standard (11-bit) CAN frame."""
    pass


class ExtendedCANMessage(CANMessage):
    """Extended (29-bit) CAN frame."""
    pass
