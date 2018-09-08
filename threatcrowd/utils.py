import modules
import requests, json, time



'''
This module has all the functions required to access and process the data from Threat Connect
'''

#TODO: Add some way to see if the domain processed is actually a sub-domain, process them differently
#TODO: Validate the type of data for MD5, Domains, Emails, IP
#TODO: Double check to see if md5s can be connected to an email address
#TODO: Add way to find malware name from the md5 hash


def get_TC_email(email):
    '''
    Takes in an email address and ties back all the associated domains
    :param email:
    :return: associated domains
    '''
    time.sleep(10)
    result = requests.get("https://www.threatcrowd.org/searchApi/v2/email/report/",
                          params={"email": email})

    try:
        data = json.loads(result.text)

    except Exception:
        data = None
        print "[x] no data for %s" % email

    return data


def get_TC_domain(domain):
    '''
    Feed it a domain and it looks up on Threat Community
    :param domain:
    :return: the jSON values from the response from threatcrowd
    '''
    time.sleep(10)

    print('requesting info from Threat Crowd')
    result = requests.get("https://www.threatcrowd.org/searchApi/v2/domain/report/", params={"domain": domain})

    print('Threat Crowd status: %s') % result.status_code

    try:
        data = json.loads(result.text)

    except Exception:
        data = None
        print "[x] no data for %s" % domain

    return data


def get_TC_hash(file_hash):

    time.sleep(10)

    result = requests.get('https://www.threatcrowd.org/searchApi/v2/file/report', params={"resource":file_hash})

    try:
        data = json.loads(result.text)
    except Exception:
        data = None
        print "[x] no data for %s" % file_hash

    return data


def get_TC_IP(ip_address):
    # Got to be respectful of rate limits
    time.sleep(10)

    result = requests.get('https://www.threatcrowd.org/searchApi/v2/ip/report', params={'ip':ip_address})

    try:
        data = json.loads(result.text)
    except Exception:
        data = None
        print "[x] no data for %s" % ip_address

    return data


def get_TC_malware_name(malware):

    time.sleep(10)

    result = requests.get('https://www.threatcrowd.org/searchApi/v2/antivirus/report', paramas={'antivirus': malware})

    try:
        data = json.loads(result.text)
    except Exception:
        data = None
        print "[x] no data for %s" %malware
    return data


def add_domain_lookup(domain):
    # Add the nodes

    domain_maker = modules.DomainTC()
    hash_maker = modules.Hashes_TC()
    email = modules.EmailTC()
    sub_domain = modules.Sub_DomainTC()
    ip_address = modules.IP_addressTC()

    # add the relationships

    domain_to_hash = modules.Domains_Hashes_Relationship()
    domain_to_sub_domain = modules.Domain_Sub_domain_Relationship()
    domain_to_email = modules.Email_Domain_TC_Relationship()
    domain_to_ip = modules.Domain_to_IP_address()

    # add the domain
    domain_maker.create_or_update(key=domain)

    # Do the look up
    data = get_TC_domain(domain)

    if data:

        if data['emails']:
            for email_address in data['emails']:

                email.create_or_update(email_address)
                domain_to_email.make_relationship(to_node=domain, from_node=email_address)

        if data['resolutions']:
            for resolve in data['resolutions']:

                resolved = {}

                resolved['last_resolved']= resolve['last_resolved']

                ip_address.create_or_update(key=resolve['ip_address'], data=resolved)

                domain_to_ip.make_relationship(from_node=domain, to_node=resolve['ip_address'])

        if data['hashes']:
            for hashes in data['hashes']:
                hash_maker.create_or_update(key=hashes)
                domain_to_hash.make_relationship(from_node=domain, to_node=hashes)

        if data['subdomains']:
            for subdomains in data['subdomains']:
                sub_domain.create_or_update(key=subdomains)
                domain_to_sub_domain.make_relationship(from_node=domain, to_node=subdomains)
    else:
        pass


def add_file_hash(file_hash):

    # Currently assumes an md5 is being sent, update it

    domain_maker = modules.DomainTC()
    hash_maker = modules.Hashes_TC()
    email = modules.EmailTC()
    sub_domain = modules.Sub_DomainTC()
    ip_address = modules.IP_addressTC()

    # add the relationships

    domain_to_hash = modules.Domains_Hashes_Relationship()
    hash_to_ip = modules.Hashes_IP_Address_Relationship()
    hash_to_subdomain = modules.Hashes_Sub_Domain_Relationship()

    # add file hash
    data = get_TC_hash(file_hash)

    hash_maker.create_or_update(key=file_hash, data={'tc_scans': data['scans']})

    if data:
        if data['ips']:
            for ip in data['ips']:
                ip_address.create_or_update(key=ip)
                hash_to_ip.make_relationship(to_node=file_hash, from_node=ip)

        if data['domains']:
            for domain in data['domains']:
                domain_maker.create_or_update(key=domain)
                domain_to_hash.make_relationship(from_node=domain, to_node=file_hash)

        if data['subdomains']:
            for subdomains in data['subdomains']:
                sub_domain.create_or_update(key=subdomains)
                hash_to_subdomain.make_relationship(from_node=file_hash, to_node=subdomains)
    else:
        pass


def add_email(email_address):

    # Create the Email object, domain object, Email_domain object
    email = modules.EmailTC()
    domain_maker = modules.DomainTC()
    email_relationship = modules.Email_Domain_TC_Relationship()

    # Need to check to see if blank
    if email_address:

        email.create_node(email_address)

        data = get_TC_email(email_address)

        if data:
            for domain in data['domains']:
                domain_maker.create_node(key=domain, data=None)
                email_relationship.make_relationship(from_node=email_address, to_node=domain)
        else:

            pass
    else:
        pass


def add_ip(ip_address):

    # Nodes
    ip_maker = modules.IP_addressTC()
    domain_maker = modules.DomainTC()
    hash_maker = modules.Hashes_TC()

    # Relationships
    ip_hash = modules.Hashes_IP_Address_Relationship()
    ip_domain = modules.Domain_to_IP_address()

    # Lets check to make sure ip_address isn't blanked or isn't "-"

    if ip_address != "-" | ip_address:

        ip_maker.create_or_update(key=ip_address)

        data = get_TC_IP(ip_address)

        if data:

            try:

                if data['resolutions']:

                    for resolve in data['resolutions']:

                        resolved = {}

                        resolved['last_resolved'] = resolve['last_resolved']

                        domain_maker.create_or_update(key=resolve['domain'], data=resolved)

                        ip_domain.make_relationship(from_node=resolve['domain'], to_node=ip_address)

                        add_domain_lookup(resolve['domain'])

                if data['hashes']:

                    for hashes in data['hashes']:

                        hash_maker.create_or_update(key=hashes)

                        ip_hash.make_relationship(to_node=hashes, from_node=ip_address)
            except:
                pass
                print "failed to parse %s" % ip_address

    else:
        pass
