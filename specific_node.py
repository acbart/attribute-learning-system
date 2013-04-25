import random
from config import RANDOM_VARIABLES, BOOLEANS, HEIGHT_MAX
from function_operators import BINARY_OPERATORS, UNARY_OPERATORS, NULLARY_OPERATORS

import itertools

class SNode(object):
    """
    A SNode is basically an operator and its arguments. If a snode has a nullary
    operator (i.e. has no arguments), then it's an attribute (e.g. other_health).

    Important properties:
        operator (function): check out function_operators.py for examples
        children (listof SNode): an immutable list of the arguments of this snode
        lock (Boolean): whether this particular snode is a nullary operator that MUST be kept during mutations.
    """

    operators_from_arity = {0 : NULLARY_OPERATORS,
                            1 : UNARY_OPERATORS,
                            2 : BINARY_OPERATORS}

    def __init__(self, operator = None, arity=None, children = None, nullary_options=None):
        """
        If an operator is NOT specified, then a random operator will be chosen. If
            an arity IS specified, an operator of the that arity will be randomly
            chosen.

        If no children are specified and no nullary_options given, then new random
        nullary nodes will be created
        as children.
        """
        if operator is None:
            if arity is None:
                operator = random.choice(NULLARY_OPERATORS +
                                         UNARY_OPERATORS +
                                         BINARY_OPERATORS)
            else:
                operator = random.choice(SNode.operators_from_arity[arity])
        self.operator = operator
        if children is None:
            children = []
            for child in xrange(operator.arity):
                children.append(SNode(arity=0))
        self.children = children

        if nullary_options is not None:
            self.nullary_options = nullary_options
        else:
            self.nullary_options = NULLARY_OPERATORS

    def mutate_index(self, current_index, mutant_index, height_left):
        """
        Find a specific snode and mutate it.
        """
        # If we've found the mutant, return a mutated version of it!
        if current_index == mutant_index:
            return self.mutate(height_left), len(self)
        else:
            # Otherwise, continue recursively searching for it.
            nodes_traversed = 1
            new_children = []
            for child in self.children:
                new_child, new_nodes_traversed = child.mutate_index(current_index+nodes_traversed,
                                                                    mutant_index,
                                                                    height_left-1)
                new_children.append(new_child)
                nodes_traversed += new_nodes_traversed
            return SNode(operator = self.operator, children = new_children, nullary_options=self.nullary_options), nodes_traversed

    def copy(self):
        """
        Returns a complete copy of this snode and its children.

        If lock is True, then also copy any lock status in the nullary nodes.
            Otherwise, turn off any locking encountered.
        """
        children_copies = [child.copy(lock) for child in self.children]
        return SNode(operator = self.operator,
                       children = children_copies, nullary_options=self.nullary_options)

    def evaluate(self, state):
        """
        Given the values specified in the *state* (a BattleState), perform the
        operation of this snode on its children.
        """
        arguments = [child.evaluate(state) for child in self.children]
        return self.operator(state, *arguments)

    def __len__(self):
        """
        Count how many subnodes are in this snode.
        """
        return 1 + sum(len(child) for child in self.children)

    def count_leaves(self):
        """
        Count how many terminal nodes (leaves, or in this case, nodes that have
        a nullary operator) are in this snode.
        """
        if self.children:
            return sum(child.count_leaves() for child in self.children)
        else:
            return 1

    def __str__(self):
        """
        Return a long string represention of this snode, with full names and
        operators.
        """
        return self.operator.formatted_name % tuple([str(child) for child in self.children])

    def short_string(self):
        """
        Return a concise string representation of this snode. Any locked nodes
        will be surronded with sigils ($).
        """
        this = ("%s") % (self.operator.short_name,)
        children = ",".join([child.short_string() for child in self.children])
        return this + "("+children+")"

    def mutate(self, height_left):
        """
        Return a mutated version of this snode.
        """

        # If we're out of room, just return a Nullary snode
        if height_left == 0:
            return self.copy()

        # Make it a child of a new parent
        new_parent = SNode(arity=1, nullary_options=self.nullary_options, children=[self.copy(),])
        return new_parent

    def cross_over(self, other, keeping):
        """
        The following Description is from:
        http://ieeexplore.ieee.org.ezproxy.lib.vt.edu:8080/stamp/stamp.jsp?tp=&arnumber=6256587

        "According to [12], the GP uniform crossover process starts
        at the tree's root node and works its way down each tree along
        some path until finding function nodes of differing arity at the
        similar location. Furthermore it can swap every node up to this
        point with its counterpart in the other tree without altering the
        structure of either. Any node in one tree having a
        corresponding node at the same location in the other is said to
        be located within the common region. Those pairs of nodes
        within the common region that have the same arity are referred
        to as interior. The common region necessarily includes all
        interior nodes. Once the interior nodes have been identified, the
        parent trees are copied. Interior nodes are selected for crossover
        with some probability which is generally set to 0.5. Crossover
        involves exchanging the selected nodes between the trees,
        while those nodes not selected for crossover remain unaffected.
        Non-interior nodes within the common region can also be
        crossed, but in this case the nodes and their subtrees are
        swapped."

        [12] Poli R., Langdon W.B. On the search properties of different crossover
        operators in genetic programming. In J. R. Koza, et al., editors, Genetic
        Programming 1998:Proceedings of the Third Annual Conference, pages
        293-301, University of Wisconsin, Madison, Wisconsin, USA, 22-25
        July 1998.
        """

        # Are we in an interior snode?
        if self.operator.arity == 0:
            return self.copy()

        if self.operator.arity == other.operator.arity and self.operator.arity:
            new_operator = random.choice((self.operator, other.operator))
            return SNode(operator=new_operator, children=self.children)
        else:
            return SNode(operator=random.choice(self.operator, other.operator), children=self.children, nullary_options=self.nullary_options)


if __name__ == "__main__":
    random.seed(5)
    a = SNode()
    print "A", a
    b = SNode()
    print "B", b
    print "Cross-over: Notice how the first node of B is used with the rest of A's nodes!"
    print "A+B", a.cross_over(b, "self")