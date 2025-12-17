import socket, struct

domain = "iwib8n7880l3p6imrbooofagu70yoped3.oastify.com"          # <-- change this to any domain you like
server = ("8.8.8.8", 53)        # DNS server (TCP)

def encode_qname(name: str) -> bytes:
    return b"".join(
        len(label).to_bytes(1, "big") + label.encode("ascii")
        for label in name.split(".")
    ) + b"\x00"

def recvn(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise RuntimeError("connection closed")
        data += chunk
    return data

# Build a simple DNS query for A record of `domain`
tid = 0x1234
header = struct.pack("!HHHHHH", tid, 0x0100, 1, 0, 0, 0)  # standard query, 1 question
question = encode_qname(domain) + struct.pack("!HH", 1, 1)  # QTYPE=A, QCLASS=IN
message = header + question
packet = struct.pack("!H", len(message)) + message         # TCP length prefix

with socket.create_connection(server) as s:
    # Send TWO DNS queries over the same TCP connection
    s.sendall(packet)
    s.sendall(packet)

    # Read TWO responses
    for i in range(2):
        length = struct.unpack("!H", recvn(s, 2))[0]
        resp = recvn(s, length)
        print(f"Response {i+1} length: {length} bytes")
