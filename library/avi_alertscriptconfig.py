#!/usr/bin/python
#
# Created on Aug 25, 2016
# @author: Gaurav Rastogi (grastogi@avinetworks.com)
#          Eric Anderson (eanderson@avinetworks.com)
# module_check: supported
# Avi Version: 17.1
#
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'status': ['preview'], 'supported_by': 'community', 'version': '1.0'}

DOCUMENTATION = '''
---
module: avi_alertscriptconfig
author: Gaurav Rastogi (grastogi@avinetworks.com)

short_description: Module for setup of AlertScriptConfig Avi RESTful Object
description:
    - This module is used to configure AlertScriptConfig object
    - more examples at U(https://github.com/avinetworks/devops)
requirements: [ avisdk ]
version_added: "2.3"
options:
    state:
        description:
            - The state that should be applied on the entity.
        default: present
        choices: ["absent","present"]
    action_script:
        description:
            - User defined alert action script.
            - Please refer to kb.avinetworks.com for more information.
    name:
        description:
            - A user-friendly name of the script.
        required: true
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Unique object identifier of the object.
extends_documentation_fragment:
    - avi
'''


EXAMPLES = '''
  - name: Create Alert Script to perform AWS server autoscaling
    avi_alertscriptconfig:
      username: ''
      controller: ''
      password: ''
      action_script: "#!/usr/bin/python\nimport sys\nfrom avi.sdk.samples.autoscale.aws_samplescaleout\
        \ import scaleout\naws_setting = {\n        'ec2_region': 'us-west-2',\n \
        \       'tenant': 'Demo',\n        'aws_access_key_id': 'ASDAS123412341234',\n\
        \        'aws_secret_access_key': '523lk45j234lk5j234;5klj',\n\
        \        'image_id': 'ami-hs343234',\n        'security_group_ids': ['sg-1234567'],\n\
        \        'subnet_id': 'subnet-91dfek3',\n        'tag': 'AviDemo',\n    \
        \    'key_name': 'demo_oregon_key'\n}\nscaleout(aws_setting, *sys.argv)"
      name: AWS-Launch-Script
      tenant_ref: Demo
'''
RETURN = '''
obj:
    description: AlertScriptConfig (api/alertscriptconfig) object
    returned: success, changed
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from avi.sdk.utils.ansible_utils import avi_common_argument_spec
    from pkg_resources import parse_version
    import avi.sdk
    sdk_version = getattr(avi.sdk, '__version__', None)
    if ((sdk_version is None) or (sdk_version and
            (parse_version(sdk_version) < parse_version('17.1')))):
        # It allows the __version__ to be '' as that value is used in development builds
        raise ImportError
    from avi.sdk.utils.ansible_utils import avi_ansible_api
    HAS_AVI = True
except ImportError:
    HAS_AVI = False


def main():
    argument_specs = dict(
        state=dict(default='present',
                   choices=['absent', 'present']),
        action_script=dict(type='str',),
        name=dict(type='str', required=True),
        tenant_ref=dict(type='str',),
        url=dict(type='str',),
        uuid=dict(type='str',),
    )
    argument_specs.update(avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (avisdk>=17.1) is not installed. '
            'For more details visit https://github.com/avinetworks/sdk.'))
    # Added api version field in ansible api.
    return avi_ansible_api(module,
            'alertscriptconfig',set([]))

if __name__ == '__main__':
    main()
