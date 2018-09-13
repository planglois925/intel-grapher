from toolkit.core import NodeCreator, RelationshipMaker
from py2neo import Graph

class Tactic(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'MITRE_Tactic'
        self.Plugin_name = 'Mitre_att&ck'
        self.node_key_field = 'ID'


class Technique(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'MITRE_Technique'
        self.Plugin_name = 'Mitre_att&ck'
        self.node_key_field = 'ID'

class Software(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'MITRE_Software'
        self.Plugin_name = 'Mitre_att&ck'
        self.node_key_field = 'ID'

class Group(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'MITRE_Group'
        self.Plugin_name = 'Mitre_att&ck'
        self.node_key_field = 'ID'

#Retiring for object defense
class DataSource(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'MITRE_DATA_SOURCE'
        self.Plugin_name = 'Mitre_att&ck'
        self.node_key_field = 'ID'

class CAPECID(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'MITRE_CAPEC'
        self.Plugin_name = 'Mitre_att&ck'
        self.node_key_field = 'ID'


class Defense(NodeCreator):
    def __init__(self):
        NodeCreator.__init__(self)
        self.Node_Label = 'MITRE_Defense'
        self.Plugin_name = 'Mitre_att&ck'
        self.node_key_field = 'ID'

#TODO Datasource -> Technique | Technique to Capec
#TODO: Do i want to extract out the mitigations into something standardized?

class Detects(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Detects"
        self.Plugin_name = "Mitre_att&ck"
        self.to_node_type = "MITRE_Technique"
        self.from_node_type = "MITRE_Defense"


class Uses(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Uses"
        self.to_node_type = "MITRE_Group"
        self.from_node_type = "MITRE_Software"

class Software_Implements(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Implements"
        self.from_node_type = "MITRE_Software"
        self.to_node_type = "MITRE_Technique"

class Accomplishes(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Accomplishes"
        self.to_node_type = "MITRE_Technique"
        self.from_node_type = "MITRE_Tactic"

class Utilize(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Accomplishes"
        self.to_node_type = "MITRE_Technique"
        self.from_node_type = "MITRE_Group"

class Has(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "Has"
        self.to_node_type = "MITRE_CAPEC"
        self.from_node_type = "MITRE_Technique"


class ByPasses(RelationshipMaker):
    def __init__(self):
        RelationshipMaker.__init__(self)
        self.Relationship_Label = "ByPasses"
        self.to_node_type = "MITRE_Defense"
        self.from_node_type = "MITRE_Technique"