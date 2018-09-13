import requests
import modules as attack_modules
import urllib

url = "https://attack.mitre.org/api.php?action=ask&format=json&query="



def get_tactics(tactic):
    #Nodes
    tactics = attack_modules.Tactic()
    techniques = attack_modules.Technique()

    #Relationships
    accomplish = attack_modules.Accomplishes()

    tactics.create_or_update(key=tactic)

    selector = "[[Has tactic::%s]]|?Has tactic|?Has ID|?Has display name|limit=9999" % tactic

    query = urllib.quote_plus(selector)

    url2 = url + query

    re = requests.get(url2)

    data = re.json()

    for t in data['query']['results']:

        techniques.create_or_update(key=t)

        accomplish.make_relationship(from_node=tactic, to_node=t, data= None)


def get_tools():

    techniques = attack_modules.Technique()

    software = attack_modules.Software()

    implements = attack_modules.Software_Implements()

    selector = "[[Category:Software]]|?Has technique|" \
               "?Has ID|?Has display name|" \
               "?Has platform|?Has alias|" \
               "?Has description|limit=9999"

    query = urllib.quote_plus(selector)

    url2 = url + query

    re = requests.get(url2)

    data = re.json()

    for soft in data['query']['results']:
        software.create_or_update(key=soft)

        for tech in data['query']['results'][soft]['printouts']['Has technique']:
            techniques.create_or_update(key=tech['fulltext'])

            implements.make_relationship(from_node=soft, to_node=tech['fulltext'], data=None)

def get_technique():
    technique = attack_modules.Technique()
    actors = attack_modules.Group()
    software = attack_modules.Software()
    tactic = attack_modules.Tactic()
    #d_source = attack_modules.DataSource()
    capicID = attack_modules.CAPECID()
    defense_tool = attack_modules.Defense()

    uses = attack_modules.Uses()
    g_to_tech = attack_modules.Utilize()
    source_to_tech = attack_modules.Detects()
    capic_to_technique = attack_modules.Has()
    tech_bypass_def = attack_modules.ByPasses()


    selector = "[[Category:Technique]]|?Has description|" \
               "?Has group|?Has ID|?Has platform|" \
               "?Has CAPEC ID|" \
               "?Has mitigation|" \
               "?Has data source|"\
               "?Bypasses defense|"\
               "?Has effective permissions|"\
               "limit=9999"
    url2 = url + urllib.quote_plus(selector)

    re = requests.get(url2)

    data = re.json()

    for tech in data['query']['results']:
        tech_data = {}

        tech_data['Platform'] = data['query']['results'][tech]['printouts']['Has platform']
        tech_data['Mitigation'] = data['query']['results'][tech]['printouts']['Has mitigation']
        tech_data["Effective permissions"] = data['query']['results'][tech]['printouts']['Has effective permissions']
        tech_data["Display Title"] = data['query']['results'][tech]['displaytitle']
        tech_data["fullurl"] = data['query']['results'][tech]["fullurl"]

        technique.create_or_update(key=tech, data=tech_data)

        if data['query']['results'][tech]['printouts']['Has data source']:
            for data_source in data['query']['results'][tech]['printouts']['Has data source']:
                defense_tool.create_or_update(key=str(data_source).lower())
                source_to_tech.make_relationship(to_node=tech, from_node=str(data_source).lower(), data=None)

        if data['query']['results'][tech]['printouts']['Has CAPEC ID']:
            for capec in data['query']['results'][tech]['printouts']['Has CAPEC ID']:
                capicID.create_or_update(key=capec)
                capic_to_technique.make_relationship(to_node=capec, from_node=tech, data=None)

        if data['query']['results'][tech]['printouts']['Bypasses defense']:
            for defense in data['query']['results'][tech]['printouts']['Bypasses defense']:
                defense_tool.create_or_update(key=str(defense).lower())
                tech_bypass_def.make_relationship(from_node=tech, to_node=str(defense).lower(), data=None)





def get_groups():
    actors = attack_modules.Group()
    software = attack_modules.Software()
    technique = attack_modules.Technique()


    uses = attack_modules.Uses()
    g_to_tech  = attack_modules.Utilize()

    selector = "[[Category:Group]]|?Uses software|" \
               "?Has technique|?Has ID|" \
               "?Has display name|" \
               "?Has alias|" \
               "?Has description| limit=9999"

    query = urllib.quote_plus(selector)

    url2 = url + query

    re = requests.get(url2)

    data = re.json()

    for group in data['query']['results']:
        actors.create_or_update(key=group)

        for tech in data['query']['results'][group]['printouts']['Has technique']:
            technique.create_or_update(key=tech['fulltext'])

            g_to_tech.make_relationship(from_node=group, to_node=tech['fulltext'], data=None)

        for soft in data['query']['results'][group]['printouts']['Uses software']:
            software.create_or_update(key=soft['fulltext'])

            uses.make_relationship(from_node=soft['fulltext'], to_node=group, data=None)

