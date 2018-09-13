from threatcrowd.modules import IP_addressTC, DomainTC,Sub_DomainTC,Hashes_TC
from threatcrowd.modules import Domain_Sub_domain_Relationship, Domain_to_IP_address, Domains_Hashes_Relationship
import requests
import time

#TODO: if you don't have the right query in the queryset
#TODO: add the query for URI
#TODO: fix the parsing of

def threatminer_domain_WHOIS(results, domain):
    update = {}

    data = results['results'][0]['last_updated']
    update['last_update'] = data
    dom = DomainTC()

    dom.create_or_update(domain, data=update)

def tm_domain_Passive(results, domain):
    ip = IP_addressTC()
    ip_to_dom = Domain_to_IP_address()

    print('[] searching for IP domains')

    if results['results']:
        for addr in results['results']:
            ip.create_or_update(addr['ip'])
            ip_to_dom.make_relationship(to_node=addr['ip'], from_node=domain)
    else:
        print('][ failed')
        pass


#def tm_domain_URI(results):

def tm_domain_Hashes(results):
    pass
def tm_domain_sub(results, domain):
    sub = Sub_DomainTC()
    d_sub = Domain_Sub_domain_Relationship()

    for result in results['results'][0]:

        sub.create_or_update(result)
        d_sub.make_relationship(from_node=domain, to_node=result)

def tm_domain_tags(results):
    pass
def threatminer_domain(domain, query):

    tm_domain = DomainTC()

    queryset= {'WHOIS': 1,
               'Passive':2,
               'URI': 3,
               'Hashes':4,
               'Sub':5,
               'Tags': 6,
               'All': 'All'}

    if query not in queryset:
        print('provide one of the following options [WHOIS, Passive, URI, Hashes, Sub, Tags, ALL]')

    tm_domain.create_or_update(domain)

    querytype = queryset[query]

    if querytype == 'All':
        i = 1
        while i < 7:

            url = 'https://api.threatminer.org/v2/domain.php?q=%s&rt=%s' % (domain, i)
            print('[] sending request to threat miner')

            results = requests.get(url).json()
            print('[x] request from threat miner received')
            if i == 1:
                threatminer_domain_WHOIS(results, domain)

            if i == 2:
                tm_domain_Passive(results=results, domain=domain)

            if i == 5:
                tm_domain_sub(results, domain)


            time.sleep(10)
            i += 1


    if query == 'WHOIS':

        url = 'https://api.threatminer.org/v2/domain.php?q=%s&rt=%s' % (domain, 1)
        print('[] sending request to threat miner')

        results = requests.get(url).json()
        print('[x] request from threat miner received')
        threatminer_domain_WHOIS(results, domain)

    if query == 'Passive':
        url = 'https://api.threatminer.org/v2/domain.php?q=%s&rt=%s' % (domain, 2)
        print('[] sending request to threat miner')

        results = requests.get(url).json()
        print('[x] request from threat miner received')
        tm_domain_Passive(results=results, domain=domain)

    if query == 'Sub':
        url = 'https://api.threatminer.org/v2/domain.php?q=%s&rt=%s' % (domain, 2)
        print('[] sending request to threat miner')

        results = requests.get(url).json()
        print('[x] request from threat miner received')
        tm_domain_sub(results, domain)

    else:
        print('invalid selection')
