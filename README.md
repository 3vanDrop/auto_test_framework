# Auto Test Framework (CAN/UDS)

A lightweight Python framework for automotive CAN/UDS validation.  
Leverages python-can for CAN I/O and Scapy for ISO-TP/UDS parsing.

## Requirements

- Docker
- Vector CANoe (optional, for real-hardware testing with Vector interfaces)
- Linux (for virtual CAN `vcan0`) or physical CAN adapters
- Python 3.8+

## Installation

```bash
git clone https://.../auto_test_framework.git
cd auto_test_framework
docker build -t auto_test_framework .
```

## Running Tests
```bash
docker run --rm --cap-add=NET_ADMIN auto_test_framework
```

## Mermaid.js Flowchart
```bash
flowchart TD
    A[Start Test] --> B[Build UDS 0x22 Request]
    B --> C[Send CAN Frame via python-can]
    C --> D[Wait for Response]
    D -->|Timeout| E[Fail: No Response]
    D -->|Received| F[Parse with Scapy ISOTP_Rsp]
    F --> G{Service ID == 0x62?}
    G -->|No| H[Fail: Unexpected Service]
    G -->|Yes| I[Extract DID Data]
    I --> J[Assert Expected Data]
    J --> K[Test Pass]
```

## Extensibility
- Add more UDS services in framework/uds/service.py.
- Implement ECU simulators/mocks via can-utils or Vector CANoe CAPL scripts.
- Integrate into CI/CD pipelines for automated regression testing.
