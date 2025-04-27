import os
import sys
import argparse
from urllib.request import urlopen

import boto3

ec2 = boto3.client('ec2')


def _first(list_obj):
    return next(iter(list_obj), None)


def _get_whitelist_group_id():    
    whitelist_group_id = os.environ.get('WHITELIST_GROUP_ID')
    if not whitelist_group_id:
        raise Exception('There is no set WHITELIST_GROUP_ID')
    return whitelist_group_id


def _make_ip_range(description, ip, is_cidr=False):
    if not is_cidr:
        ip = ip + '/32'
    return {
        'Description': description,
        'CidrIp': ip,
    }


def _add_ip_range_to_whitelist(description, ip):
    ec2.authorize_security_group_ingress(
        GroupId=_get_whitelist_group_id(),
        IpPermissions=[
            {
                'IpProtocol': '-1',
                'IpRanges': [_make_ip_range(description, ip)],
            },
        ],
    )


def _get_rule_from_whitelist(description):
    response = ec2.describe_security_group_rules(
        Filters=[{'Name': 'group-id', 'Values': [_get_whitelist_group_id()]}],
    )
    rules = response['SecurityGroupRules']
    return _first([rule for rule in rules if rule.get('Description') == description])


def _remove_rule_from_whitelist(rule):
    ec2.revoke_security_group_ingress(
        GroupId=_get_whitelist_group_id(),
        IpPermissions=[
            {
                'IpProtocol': '-1',
                'IpRanges': [
                    _make_ip_range(
                        rule.get('Description'),
                        rule.get('CidrIpv4'),
                        is_cidr=True,
                    ),
                ],
            },
        ],
    )


def _update_whitelist_rule(description, ip):
    existing_rule = _get_rule_from_whitelist(description)
    if existing_rule:
        _remove_rule_from_whitelist(existing_rule)
    _add_ip_range_to_whitelist(description, ip)


def _get_my_ip():
    with urlopen('https://checkip.amazonaws.com/') as response:
        return response.read().decode('utf-8').strip()


def main():
    """
    Main function to update the whitelist rule of a security group.
    
    This function parses command-line arguments to update the security group whitelist
    with a specified IP address and rule description. The `--description` argument is required
    to provide a description for the rule, while the `--ip` argument is optional and specifies
    the IP address to be added to the whitelist. If the IP address is not provided, a default
    value or behavior may be applied.

    Note:
    - Don't forget to set your AWS environment as needed.

    Usage:
    - export WHITELIST_GROUP_ID='sg-xxxxxxxxx'  # Set your security group ID
    - python app.py --description [Rule Description] --ip [Your IP] [Optional]
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--description', type=str)
    parser.add_argument('--ip', type=str)

    args = parser.parse_args()
    if not args.description:
        raise Exception('There is no set description')

    ip = args.ip
    if not ip:
        ip = _get_my_ip()

    _update_whitelist_rule(args.description, ip)


if __name__ == '__main__':
    main()
