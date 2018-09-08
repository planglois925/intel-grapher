from core.modules import NodeCreator, RelationshipMaker
from py2neo import Graph


class EmailTC(NodeCreator):

    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'Email'
        self.Plugin_name = 'ThreatConnect'
        self.node_key_field = 'email_address'

class DomainTC(NodeCreator):

    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'Domain'
        self.Plugin_name = 'ThreatConnect'
        self.node_key_field = 'domain'


class Sub_DomainTC(NodeCreator):

    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'Sub-Domain'
        self.Plugin_name = 'ThreatConnect'
        self.node_key_field = 'sub-domain'



class IP_addressTC(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'IP_address'
        self.Plugin_name = 'ThreatConnect'
        self.node_key_field = 'ip_address'


class Hashes_TC(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'Hashes'
        self.Plugin_name = 'ThreatConnect'
        self.node_key_field = 'Hashes'


#Relationships

class Domain_to_IP_address(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Resolves"
        self.to_node_type = "IP_address"
        self.from_node_type = "Domain"


class Domain_Sub_domain_Relationship(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Hosts"
        self.to_node_type = "Sub-Domain"
        self.from_node_type = "Domain"

class Email_Domain_TC_Relationship(RelationshipMaker):

    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Owns"
        self.to_node_type = "Domain"
        self.from_node_type = "Email"

class Domains_Hashes_Relationship(RelationshipMaker):

    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Associated"
        self.to_node_type = "Hashes"
        self.from_node_type = "Domain"

class Hashes_IP_Address_Relationship(RelationshipMaker):

    def __init__(self):
        NodeCreator.__init__(self)
        self.Relationship_Label = "Associated"
        self.to_node_type = "Hashes"
        self.from_node_type = "IP_address"


class Hashes_Sub_Domain_Relationship(RelationshipMaker):

    def __int__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Associated"
        self.to_node_type = "Hashes"
        self.from_node_type = "sub-domain"