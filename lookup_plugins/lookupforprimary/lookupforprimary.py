# lookupforprimary: lookup the primary member of a MongoDB replica set
# Copyright (C) 2016  Olivier Perbellini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)

import time

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from pymongo import MongoClient

__metaclass__ = type

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        """
        Usage: {{ lookup('lookupforprimary', 'ip') }}
        :param terms: contain the ip to connect to MongoDB
        :param variables: contains the variables available to ansible at the time the lookup is templated
        :param kwargs: keyword arguments
        :return: the replica set primary member ip whether it exist or throw an AnsibleError
        """
        ret = []
        ip = terms[0]
        client = MongoClient(ip, 27017)
        try:
            primary_checks_remaining = 4
            primary = None
            while not primary and primary_checks_remaining > 0:
                primary = self.get_replica_primary_host(client)
                primary_checks_remaining -= 1
                time.sleep(5)
        finally:
            client.close()
        if not primary:
            raise AnsibleError('Unable to get the primary member')
        primary_ip = primary.split(':')[0]
        ret.append(primary_ip)
        display.debug(ret[0])
        return ret

    @staticmethod
    def get_replica_primary_host(client):
        """
        Execute the "isMaster" command using the given 'client' and retrieve the value of the "primary" key
        :param client: the MongoDB client to use
        :return: return None or the primary information in the format: "host:port"
        """
        return client.admin.command('isMaster').get('primary')
