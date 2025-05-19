FROM python:3.10-slim

# Install CAN utilities and Python deps
RUN apt-get update && \
    apt-get install -y can-utils iproute2 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Setup virtual CAN interface
RUN modprobe vcan && \
    ip link add dev vcan0 type vcan && \
    ip link set up vcan0

ENTRYPOINT ["pytest", "--maxfail=1", "--disable-warnings", "-q"]
