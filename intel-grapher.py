from threatcrowd import utils as tc_utils
from threatminer import utils as tm_utils
import argparse


def main():

    parser = argparse.ArgumentParser(description='Tool to take data and insert it into graphdatabase')
    parser.add_argument('-d', '--domain', help="Domains to look up", default=None)
    parser.add_argument('-e', '--email',help='Emails to look up', default=None)
    parser.add_argument('-hx', '--hash', help='Hashes to look up', default=None)
    parser.add_argument('-i', '--ip', help='IP address to look up', default=None)
    parser.add_argument('-s', '--source', help='Which sources to pick from', choices=['tc','tm','all'])

    args = parser.parse_args()

    if args.domain:
        if args.source == 'tc':
            tc_utils.add_domain_lookup(args.domain)
        if args.source == 'tm':
            tm_utils.threatminer_domain(domain=args.domain, query='All')
        if args.source == 'all':
            tm_utils.threatminer_domain(domain=args.domain, query='All')
            tc_utils.add_domain_lookup(args.domain)

    if args.email:
        tc_utils.add_email(args.email)
    if args.hash:
        tc_utils.add_file_hash(args.hash)

if __name__ == '__main__':
    main()

