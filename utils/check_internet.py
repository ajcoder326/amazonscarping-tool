import socket
def check_internet() -> bool:
    """
    Check if the machine has an active internet connection by attempting 
    to connect to Google's public DNS server (8.8.8.8) on port 53.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        socket.setdefaulttimeout(5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("8.8.8.8", 53))
        return True
    except (socket.timeout, socket.gaierror, socket.error):
        return False


