import math
from ipaddress import AddressValueError, IPv4Address
from netsec.utils import timeout

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
    @timeout()
    def validate_input(i1, i2):
        """
        Validate and sanitize the input values i1 and i2, and return the results of the computations.

        Args:
            i1 (float): The first input value.
            i2 (float): The second input value.

        Returns:
            tuple: The results of the computations (i1/i2, i1**i2).

        Raises:
            ValueError: If the division by zero is attempted or if the base is 0 and the exponent is negative.
            OverflowError: If the resulting power or division is too large.
            TimeoutError: If the computation takes more than 1 second.

        Example:
        >>> Sanitizer.validate_input(2.0, 3.0)
        (0.6666666666666666, 8.0)
        """
        if i2 == 0:
            raise ValueError("Division by zero is not allowed")
        
        if i1 == 0 and i2 < 0:
            raise ValueError("0 raised to a negative power is undefined")

        try:
            power_result = math.pow(i1, i2)
        except OverflowError:
            raise OverflowError("Resulting power is too large")

        division_result = i1 / i2

        if math.isinf(division_result):
            raise OverflowError("Resulting division is too large")
        if math.isnan(division_result):
            raise ValueError("Resulting division is not a number")

        return division_result, power_result

