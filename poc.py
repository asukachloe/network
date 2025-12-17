import socket, struct

domain = "8z81bdaybqotswlcu1rer5d6xx3orfj38.oastify.com"  # change this to any domain you like

def encode_qname(name):
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

def default_dns_server(port=53):
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    return (line.split()[1].strip(), port)
    except FileNotFoundError:
        pass
    return ("127.0.0.1", port)

server = default_dns_server()

tid = 0x1234
header = struct.pack("!HHHHHH", tid, 0x0100, 1, 0, 0, 0)  # standard query
question = encode_qname(domain) + struct.pack("!HH", 1, 1)  # A, IN
msg = header + question
packet = struct.pack("!H", len(msg)) + msg  # TCP length prefix

with socket.create_connection(server) as s:
    # send TWO DNS queries over one TCP connection
    s.sendall(packet)
    s.sendall(packet)

    for i in range(2):
        length = struct.unpack("!H", recvn(s, 2))[0]
        resp = recvn(s, length)
        print(f"Response {i+1} length:", length)
