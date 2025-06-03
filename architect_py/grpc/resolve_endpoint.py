import ipaddress
import logging
from typing import Tuple, cast
from urllib.parse import urlparse

import dns.asyncresolver
import dns.resolver
from dns.rdtypes.IN.SRV import SRV

PAPER_GRPC_PORT = 10081


async def resolve_endpoint(
    endpoint: str, paper_trading: bool = True
) -> Tuple[str, int, bool]:
    """
    From a gRPC endpoint, resolve the host, port and whether or not the endpoint
    should use SSL.  If the port is specified explicitly, it will be used.  Otherwise,
    try to look up the port using the host's DNS SRV record.

    If no SRV DNS record exists, or the hostname is an IP address, port will be None.

    If the endpoint scheme is https, or the hostname matches *.architect.co,
    return True for use_ssl.  Otherwise, return False.

    Example outputs:

    Assuming a SRV DNS record exists for app.architect.co pointing to port 8081.

    | Endpoint | Host | Port | Use SSL |
    |----------|------|------|---------|
    | https://app.architect.co:8081 | app.architect.co | 8081 | True |
    | http://app.architect.co:8081 | app.architect.co | 8081 | False |
    | app.architect.co | app.architect.co | 8081 | True |
    | localhost:9000 | localhost | 9000 | False |
    """
    if "://" not in endpoint:
        endpoint = f"unknown://{endpoint}"
    url = urlparse(endpoint)

    if url.hostname is None:
        raise ValueError(f"Invalid endpoint, missing hostname: {endpoint}")

    use_ssl = url.scheme == "https" or (
        url.scheme != "http" and url.hostname.endswith(".architect.co")
    )

    try:
        _ = ipaddress.ip_address(url.hostname)
        if url.port is None:
            raise ValueError(
                f"Invalid endpoint, target is an IP address but missing port: {endpoint}"
            )
        return url.hostname, url.port, url.scheme == "https"
    except ValueError:
        # not an IP address
        pass

    if url.port is not None:
        return url.hostname, url.port, use_ssl

    logging.info(f"No port specified for {endpoint}, looking up DNS SRV records...")
    srv_records: dns.resolver.Answer = await dns.asyncresolver.resolve(
        url.hostname, "SRV"
    )
    if len(srv_records) == 0:
        raise Exception(f"No SRV records found for {url.hostname}")

    record = cast(SRV, srv_records[0])
    logging.info(f"Found {endpoint}: {record.target}:{record.port}")

    host = str(record.target).rstrip(".")  # strips the period off of FQDNs

    port = record.port
    if paper_trading:
        if "app.architect.co" in host or "staging.architect.co" in host:
            port = PAPER_GRPC_PORT

    return host, port, use_ssl
