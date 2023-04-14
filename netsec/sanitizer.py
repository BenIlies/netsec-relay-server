from ipaddress import AddressValueError, IPv4Address

class Sanitizer:
    @staticmethod
    def validate_ip(ip, check_specific_ips=False):
        """
        Validate the given IP address.

        Args:
            ip (str): The IP address to validate.
            check_specific_ips (bool, optional): Check for specific IP addresses like multicast, reserved, or unspecified.
                Defaults to False.

        Raises:
            ValueError: If the IP address is invalid, multicast, reserved, or unspecified.

        Example:
        >>> Sanitizer.validate_ip("127.0.0.1")
        """
        try:
            ipv4 = IPv4Address(ip)
            if check_specific_ips and (ipv4.is_multicast or ipv4.is_reserved or ipv4.is_unspecified):
                raise ValueError(f"Invalid IP address: {ip}")
        except AddressValueError as e:
            raise ValueError(f"Invalid IP address: {ip}")



    @staticmethod
    def validate_port(port):
        """
        Validate the given port number.

        Args:
            port (int): The port number to validate.

        Raises:
            ValueError: If the port number is not within the valid range (1-65535).

        Example:
        >>> Sanitizer.validate_port(8080)
        """
        if not 1 <= port <= 65535:
            raise ValueError(f"Invalid port number: {port}")

    @staticmethod
    def validate_input(i1, i2):
        """
        Validate the input values i1 and i2.

        Args:
            i1 (int): The first input value.
            i2 (int): The second input value.

        Raises:
            ValueError: If the division by zero is attempted or the second input value is too large.
            OverflowError: If the resulting power is too large.

        Example:
        >>> Sanitizer.validate_input(2, 3)
        """
        if i2 == 0:
            raise ValueError("Division by zero is not allowed")

        if i2 > 10000:
            raise ValueError("Second input value too large")

        try:
            i1 ** i2
        except OverflowError:
            raise OverflowError("Resulting power is too large")
