from .message import StandardCANMessage, ExtendedCANMessage


class CANMessageFactory:
    """Factory for creating standard or extended CAN messages."""
    @staticmethod
    def create(arbitration_id: int, data: bytes, is_extended_id: bool = False):
        if is_extended_id:
            return ExtendedCANMessage(arbitration_id, data, True)
        return StandardCANMessage(arbitration_id, data, False)
