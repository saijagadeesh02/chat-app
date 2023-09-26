
from collections import defaultdict


class ClientConnectionDB:
    connection_map = defaultdict(list)


class ClientNamespaces:
    namespace_map = {
        # sid : client_socket_namespace
    }