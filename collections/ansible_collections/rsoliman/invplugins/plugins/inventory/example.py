from ansible.plugins.inventory import BaseInventoryPlugin

ANSIBLE_METADATA = {
    'metadata_version': '',
    'status': [],
    'supported_by': ''
}

DOCUMENTATION = '''
---
module:
plugin_type:
short_description:
version_added: ""
description:
options:
author:
'''


class InventoryModule(BaseInventoryPlugin):
    """An example inventory plugin."""

    NAME = 'FQDN_OF_THE_PLUGIN_GOES_HERE'

    def verify_file(self, path):
        """Verify that the source file can be processed correctly.

        Parameters:
            path:AnyStr The path to the file that needs to be verified

        Returns:
            bool True if the file is valid, else False
        """
        return True

    def _get_raw_host_data(self):
        """Get the raw static data for the inventory hosts

        Returns:
            dict The host data formatted as expected for an Inventory Script
        """
        return {
            "all": {
                "hosts": ["web1.example.com", "web2.example.com"]
            },
            "_meta": {
                "hostvars": {
                    "web1.example.com": {
                        "ansible_user": "rdiscala"
                    },
                    "web2.example.com": {
                        "ansible_user": "rdiscala"
                    }
                }
            }
        }
    
    def parse(self, inventory, loader, path, cache=True):
        """Parse and populate the inventory with data about hosts.

        Parameters:
            inventory The inventory to populate
        """
        # The following invocation supports Python 2 in case we are
        # still relying on it. Use the more convenient, pure Python 3 syntax
        # if you don't need it.
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        raw_data = self._get_raw_host_data()
        _meta = raw_data.pop('_meta')
        for group_name, group_data in raw_data.items():
            for host_name in group_data['hosts']:
                self.inventory.add_host(host_name)
                for var_key, var_val in _meta['hostvars'][host_name].items():
                    self.inventory.set_variable(host_name, var_key, var_val)