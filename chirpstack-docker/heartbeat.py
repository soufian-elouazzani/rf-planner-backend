import socket
import time
import json
import random

# CONFIGURATION
BRIDGE_IP = "127.0.0.1"  # Or 'localhost'
BRIDGE_PORT = 1700
# Add your Gateway IDs from your ChirpStack UI here

GATEWAY_COORDINATES = {
    "1817e387a485c532": {"lat": 48.8566, "long": 2.3522, "alti": 35},  # Center
    "3307a3c57d2ee1bb": {"lat": 48.8800, "long": 2.3700, "alti": 50},  # North-East
    "f8fb0163897e5d47": {"lat": 48.8300, "long": 2.3300, "alti": 20},  # South
    "07f42c0865db55e3": {"lat": 48.8600, "long": 2.2900, "alti": 45},  # West
    "cda412c8deed33c5": {"lat": 48.8400, "long": 2.3900, "alti": 60}   # East
}

def send_heartbeat(gw_id):
    # Standard LoRaWAN UDP Header for 'Stat' messages
    # Protocol Version 2 | Random Token | PUSH_DATA Identifier (0x00)
    coords = GATEWAY_COORDINATES.get(gw_id)
    token = random.randint(0, 65535).to_bytes(2, 'big')
    header = b'\x02' + token + b'\x00' + bytes.fromhex(gw_id)
    payload = {
        "stat": {
            "time": time.strftime("%Y-%m-%d %H:%M:%S GMT"),
            "lati": coords["lat"],
            "long": coords["long"],
            "alti": coords["alti"],
            "ackr": 100.0,
            "rxnb": 1,
            "rxfw": 1,

        }
    }
    
    packet = header + json.dumps(payload).encode()
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(packet, (BRIDGE_IP, BRIDGE_PORT))
        print(f"✅ Sent heartbeat for Gateway: {gw_id}")

if __name__ == "__main__":
    print("🚀 Starting Simulation... Press CTRL+C to stop.")
    while True:
        for gid in GATEWAY_COORDINATES:
            send_heartbeat(gid)
        time.sleep(30) # ChirpStack usually expects stats every 30s
