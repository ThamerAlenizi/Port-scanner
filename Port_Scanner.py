import argparse
import socket

def main():
    try:
        parser = argparse.ArgumentParser(description="Script to take IP or domain name and port as arguments")
        parser.add_argument('-T', '--target', type=str, required=True, help='IP address or domain name to connect to')
        parser.add_argument('-p', '--port', type=int, required=False, help='Port number to connect to')
        parser.add_argument('-r', '--port-range', type=str, required=False, help='Port range to connect to (e.g. 20-80)')
        parser.add_argument('-a', '--all-ports', action='store_true', required=False, help='Scan all ports')

        args = parser.parse_args()
        target = args.target
        port = args.port
        port_range = args.port_range
        all_ports = args.all_ports

        # Resolve domain name to IP address if necessary
        try:
            ip_address = socket.gethostbyname(target)
        except socket.gaierror:
            raise ValueError(f"Could not resolve domain: {target}")

        if port and not (0 < port <= 65535):
            raise ValueError("Error! The port number is out of range")

        if port_range:
            if '-' in port_range:
                start_port, end_port = map(int, port_range.split('-'))
                if not (0 < start_port <= 65535) or not (0 < end_port <= 65535):
                    raise ValueError("Error! Port range is out of range")
            else:
                raise ValueError("Error! Port range format is incorrect. Use start-end format (e.g. 20-80)")

        # Perform the scans based on provided arguments
        if not all_ports:
            if port:
                port_scanning_single_port(ip_address, port)
            if port_range:
                port_scanning_specific_range(ip_address, start_port, end_port)
        else:
            port_scanning_all_ports(ip_address)

    except ValueError as e:
        print(e)

def port_scanning_single_port(IP, port):
    print(f"Scanning port {port} on {IP}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        status = sock.connect_ex((IP, port))
        if status == 0:
            print(f"Port {port} is OPEN")
            with open("single_port_scan.txt", "a") as fOut:
                fOut.write(f"{port} : OPEN\n")
        else:
            print(f"Port {port} is CLOSED")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    finally:
        sock.close()

def port_scanning_specific_range(IP, begin, end):
    print(f"Scanning ports {begin} to {end} on {IP}")
    try:
        with open("ranged_port_scan.txt", "a") as fOut:
            for port in range(begin, end + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                status = sock.connect_ex((IP, port))
                if status == 0:
                    print(f"Port {port} is OPEN")
                    fOut.write(f"{port} : OPEN\n")
                else:
                    print(f"Port {port} is CLOSED")
                sock.close()  # Close socket after each scan
    except Exception as e:
        print(f"Error scanning range: {e}")

def port_scanning_all_ports(IP):
    print(f"Scanning all ports (1-65535) on {IP}")
    try:
        with open("all_ports_scan.txt", "a") as fOut:
            for port in range(1, 65536):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                status = sock.connect_ex((IP, port))
                if status == 0:
                    print(f"Port {port} is OPEN")
                    fOut.write(f"{port} : OPEN\n")
                sock.close()  # Close socket after each scan
    except Exception as e:
        print(f"Error scanning all ports: {e}")

if __name__ == "__main__":
    main()
