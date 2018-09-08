
from py2neo import Graph, Node, Relationship



class NodeCreator:

    def __init__(self):

        '''
        Start off my creating the graph connection
        If you're making a new Node label define it here, along with it's abbreviation
        '''
        #CHANGE ME TO WHATEVER YOURS IS
        self.graph = Graph(password="password")
        self.Node_Label = ""
        self.Node_abrev = ""
        self.node_fields = []
        self.Plugin_name = ""
        self.node_key_field = ""

    def create_or_update(self, key, data=None):
        """
        Method to create or update a node.
        :param key: THe unique key value that you want to add or update
        :param data:  The data that you want to be added to the node
        :return:
        """

        node = self.graph.find_one(self.Node_Label, 'id', key)

        if node is None:

            self.create_node(key,data)

        else:

            self.update_node(data=data, key=key)

    def create_node(self, key, data=None):
        """
        Method to add a new node to the graph database
        :param key: The unique key value that you want to use to add
        :param data: The data you want to add
        :return:
        """

        if data is None:

            node = Node(self.Node_Label, id=key)
            print 'creating node %s' % key

        else:
            node = Node(self.Node_Label, id=key)
            node.update(data)

        self.graph.create(node)

    def update_node(self,data, key):
        node = self.graph.find_one(self.Node_Label, 'id', key)
        node.update(data)


class RelationshipMaker:
    def __init__(self):

        '''
        Start off my creating the graph connection
        If you're making a new Node label define it here, along with it's abbreviation
        '''

        self.graph = Graph(password="password")
        self.Relationship_Label = ""
        self.node_fields = []
        self.Plugin_name = ""
        self.Bidirectional = False
        self.from_node_type = ""
        self.to_node_type = ""


    def make_relationship(self, from_node, to_node, data=None):

        relationship = self.Relationship_Label
        print 'search for %s' % to_node

        from_nodes = self.graph.find_one(self.from_node_type, 'id', from_node)
        end_node = self.graph.find_one(self.to_node_type, 'id', to_node)

        print "found %s" % from_nodes
        print "found end: %s" % end_node

        if from_nodes != None and end_node != None:

            rel = Relationship(from_nodes, relationship, end_node)

            if data:
                for key, value in data.iteritems():
                    rel[key] = value

            self.graph.create(rel)

        else:

            print "failed to find %s" % from_node
