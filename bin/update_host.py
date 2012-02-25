#!/usr/bin/env python
#
""" update_host
Update a single host entry in Amazon r53. If the entry doesn't exist it is created.
"""

import logging
from optparse import OptionParser
import os
import sys

import boto

from cirrus.r53 import Zone

log = logging.getLogger('cirrus')
log.addHandler(logging.StreamHandler())

def get_args(usage):
    """Sets up Option parser and then resturns the parsed options and args."""
    parser = OptionParser(usage=usage)
    parser.add_option('-a', dest='arecord', help="Set host to an a record")
    parser.add_option('-A', dest='alias', help="Route 53 Alias record, specify quoted 'HostedZoneID DNSName'")
    parser.add_option('-c', '--cname', dest='cname', help="Set host to a cname.")
    parser.add_option('-t', '--ttl', dest='ttl', type='int', default=3600, help="The ttl for this entry")
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)

    return parser.parse_args()

def main():
    usage = "usage: %prog <fqdn> [domain] <-c [cname] | -a [a record] | -A [Route 53 Alias]>"
    options, args = get_args(usage)
    if len(args) < 1 or len(args) > 2:
        print usage
        sys.exit(1)
    host = args[0] #host is fqdn
    if len(args) == 2:
        domain = args[1] #domain is zone
    else:
        if host.count('.') > 1:
            domain = host.split('.', 1)[1]
        else: #must be the domain root
            domain = host

    if not ( os.environ.has_key('AWS_ACCESS_ID') and os.environ.has_key('AWS_SECRET_KEY') ):
        log.error("Please set environment variables AWS_ACCESS_ID and AWS_SECRET_KEY")
        sys.exit(1)
    access_id = os.environ['AWS_ACCESS_ID']
    secret_key =  os.environ['AWS_SECRET_KEY']
    if options.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARN)

    if options.cname is not None:
        rtype = 'CNAME'
        value = options.cname
    elif options.arecord is not None:
        rtype = 'A'
        value = options.arecord
    elif options.alias is not None:
        rtype = 'A'
        value = 'Alias ' + options.alias
    else:
        print usage
        sys.exit(1)

    #Get the connection
    conn = boto.connect_route53(access_id, secret_key)
    r53zone = Zone(conn, domain)

    if not r53zone.exists():
        log.error('Zone ' + domain + " doesn't exist!")
        sys.exit(2)

    existing = r53zone.get_host(host)
    if existing is None:
        r53zone.create_host(host, rtype, options.ttl, value)
    else:
        r53zone.update_host(host, rtype, options.ttl, existing, value)

if __name__ == "__main__":
    sys.exit(main())
