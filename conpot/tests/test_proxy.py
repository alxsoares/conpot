# Copyright (C) 2014  Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import unittest

import gevent
import gevent.monkey

from gevent.server import StreamServer
from gevent.socket import socket

from conpot.emulators.proxy import Proxy

gevent.monkey.patch_all()

test_input = 'Hiya, this is a test'


class TestProxy(unittest.TestCase):
    def test_proxy(self):
        mock_service = StreamServer(('127.0.0.1', 0), self.echo_server)
        gevent.spawn(mock_service.start)
        gevent.sleep(1)

        proxy = Proxy('proxy', '127.0.0.1', mock_service.server_port)
        server = proxy.get_server('127.0.0.1', 0)
        gevent.spawn(server.start)
        gevent.sleep(1)

        s = socket()
        s.connect(('127.0.0.1', server.server_port))
        test_input = 'Hiya, this is a test'
        s.sendall(test_input)
        received = s.recv(len(test_input))
        self.assertEqual(test_input, received)
        mock_service.stop(1)

    def test_ssl_proxy(self):
        # TODO
        pass

    def echo_server(self, sock, address):
        r = sock.recv(len(test_input))
        sock.send(r)