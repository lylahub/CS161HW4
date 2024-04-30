##############
# Homework 4 #
##############

# Exercise: Fill this function.
# Returns the index of the variable that corresponds to the fact that
# "Node n gets color c" when there are k possible colors
def node2var(n, c, k):
    """
    Calculate the variable index for a given node and color in a graph coloring problem.
    This function computes the index used to represent the fact that "Node n gets color c" 
    in a graph where each node can be colored with one of k possible colors.

    Parameters:
    n (int): The node number
    c (int): The color assigned to the node
    k (int): The total number of available colors

    Returns:
    int: The unique index representing the color assignment for the node.
    """
    return (n-1) * k + c

# Exercise: Fill this function
# Returns *a clause* for the constraint:
# "Node n gets at least one color from the set {1, 2, ..., k}"
def at_least_one_color(n, k):
    """
    Create a clause that ensures node n is assigned at least one color out of k available colors.
    This function returns a list of variable indices, each representing a color assignment for node n,
    forming an OR clause where at least one color must be selected.

    Parameters:
    n (int): The node number.
    k (int): Number of possible colors.

    Returns:
    list[int]: List of variable indices for the OR clause.
    """
    c = []
    for colors in range(1, k+1):
        var = node2var(n, colors, k)
        c.append(var)
    return c

# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets at most one color from the set {1, 2, ..., k}"
def at_most_one_color(n, k):
    """
    Generate clauses ensuring node n gets at most one of k colors.
    Forms pairwise negations for all color combinations, representing mutual exclusivity.

    Parameters:
    n (int): Node number.
    k (int): Number of colors.

    Returns:
    list[list[int]]: List of clauses, each clause being a list of negated variable indices.
    """
    c = []
    for i in range(1, k+1):
        for j in range(i+1, k+1):
            var_i = node2var(n,i,k)
            var_j = node2var(n,j,k)
            c.append([-var_i, -var_j])
    return c

# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets exactly one color from the set {1, 2, ..., k}"
def generate_node_clauses(n, k):
    """
    Generate clauses ensuring node n gets exactly one color out of k.

    Combines clauses for 'at least one' and 'at most one' color assignments.

    Parameters:
    n (int): Node number.
    k (int): Number of colors.

    Returns:
    list[list[int]]: Clauses enforcing the exact one color constraint.
    """
    c = []
    c.append(at_least_one_color(n,k))
    c.extend(at_most_one_color(n,k))
    return c

# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Nodes connected by an edge e cannot have the same color"
# The edge e is represented by a tuple
def generate_edge_clauses(e, k):
    """
    Generate clauses for the constraint that connected nodes m and n cannot share the same color.

    Forms negations for each color, ensuring nodes in edge e don't get colored identically.

    Parameters:
    e (tuple): Edge connecting nodes m and n.
    k (int): Number of colors.

    Returns:
    list[list[int]]: Clauses enforcing the different colors constraint.
    """
    m, n = e
    c = []
    for i in range(1, k+1):
        m_c = node2var(m, i, k)
        n_c = node2var(n, i, k)
        c.append([-m_c, -n_c])
    return c

# The function below converts a graph coloring problem to SAT
# Return CNF as a list of clauses
# DO NOT MODIFY
def graph_coloring_to_sat(graph_fl, sat_fl, k):
    clauses = []
    with open(graph_fl) as graph_fp:
        node_count, edge_count = tuple(map(int, graph_fp.readline().split()))
        for n in range(1, node_count + 1):
            clauses += generate_node_clauses(n, k)
        for _ in range(edge_count):
            e = tuple(map(int, graph_fp.readline().split()))
            clauses += generate_edge_clauses(e, k)
    var_count = node_count * k
    clause_count = len(clauses)
    with open(sat_fl, 'w') as sat_fp:
        sat_fp.write("p cnf %d %d\n" % (var_count, clause_count))
        for clause in clauses:
            sat_fp.write(" ".join(map(str, clause)) + " 0\n")
    return clauses, var_count


# Example function call
if __name__ == "__main__":
   graph_coloring_to_sat("graph1.txt", "graph1_3.cnf", 3)
   graph_coloring_to_sat("graph1.txt", "graph1_4.cnf", 4)
   graph_coloring_to_sat("graph2.txt", "graph2_3.cnf", 3)
   graph_coloring_to_sat("graph2.txt", "graph2_4.cnf", 4)
   graph_coloring_to_sat("graph2.txt", "graph2_5.cnf", 5)
   graph_coloring_to_sat("graph2.txt", "graph2_6.cnf", 6)
   graph_coloring_to_sat("graph2.txt", "graph2_7.cnf", 7)
   graph_coloring_to_sat("graph2.txt", "graph2_8.cnf", 8)