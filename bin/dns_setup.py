#!/usr/bin/env python
#
""" dns_setup
Run this on a yaml dns definition an it will check the cloud to make sure your dns is setup
and if not will set it up.
"""

import logging
from optparse import OptionParser
import yaml
import sys

import boto

from cirrus.r53 import Zone

log = logging.getLogger('cirrus')
log.addHandler(logging.StreamHandler())

def get_args():
    """Sets up Option parser and then resturns the parsed options and args."""
    usage = "usage: %prog [options] <yaml definition>"
    parser = OptionParser(usage=usage)
    parser.add_option('-d', '--dry-run', action='store_true', dest='dry_run', default=False, \
        help="Report what would be done but do nothing.")
    parser.add_option('-s', '--show', action='store_true', dest='show', default=False, \
        help="Returns a bind style zone file for the defined domains.")
    parser.add_option('--terminate', action='store_true', dest='terminate', default=False, \
        help="Instead of creating zones delete them.")
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)
    parser.add_option('-q', '--quite', action='store_true', dest='quite', default=False)
    parser.add_option('--debug', action='store_true', dest='debug', default=False)

    return parser.parse_args()

def main():
    options, args = get_args()

    if options.debug:
        log.setLevel(logging.DEBUG)
    elif options.verbose:
        log.setLevel(logging.INFO)
    elif options.quite:
        log.setLevel(logging.ERROR)
    else:
        log.setLevel(logging.WARN)

    #Pull from the yaml file
    def_file = open(args[0], 'r')
    dns_def = yaml.load(def_file)
    zones = dns_def['zones']

    #Get the connection
    conn = boto.connect_route53(dns_def['access_id'], dns_def['secret_key'])

    if options.dry_run:
        log.warn("Doing a dry-run, only reporting actions.")

    for name, zone_file in zones.iteritems():
        r53zone = Zone(conn, name)
       
        if r53zone.exists():
            if options.terminate:
                r53zone.remove(options.dry_run)
            elif options.show:
                print str(r53zone)
            else:
                r53zone.update(zone_file, options.dry_run)
        elif options.show or options.terminate:
            log.warn('Zone %s does not exist' % (name))
        else:
            r53zone.create(zone_file, options.dry_run)

if __name__ == "__main__":
    sys.exit(main())
