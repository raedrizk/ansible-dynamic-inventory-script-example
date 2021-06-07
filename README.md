# A sample dynamic inventory script to be used with Ansible

A python script that queries a mysql database and creates an Ansible inventory based on the output

For more information on developing a custom inventory script, please refer the [Ansible documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#developing-inventory-scripts)

Script accepts `--hots <hostname>` and `--list` arguments as per the requirements

A sample schema dump is also provided in the `cmdb.sql` file

To use in Ansible Tower:
1. Create a custom credential type using the definition in the `mysql_cmdb_custom_credential_type_definition` file
2. Define the actual crednetial for the mydql db
3. In Ansible tower, Create a new custom inventory script source under resources using the contents of the `inventory_custom_cmdb.py` file 

Note: The script requires the python `mysql-connector` package, so make sure that the library is installed in one of the python virtual environments on all the tower nodes.

4. Create a new inventory
5. Create a new source under the new inventory that used the type `Custom Script` and reference the source created in step 3

Note: Make sure to use the correct Ansible Environment with the correct python prerequisites installed