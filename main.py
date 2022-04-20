import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
import pymetis
import numpy as np
import random
import copy
import enum
import statistics

'''
#General Algorithm
#1: Take G(original whole graph) and partition it into n contiguous proto-districts
#2: Gather all boundary connected components into set B(or lists of partition straddling edges)
#3: Select random node from B and switch with adjacent partition (check if the switch is valid)
 \ does not break up partitions repeat switch with new node if invalid (use nx.is_connected())
#4: Compute score for updated(pop/partisan lean/etc.) district config
#5 If new map is better keep changes
 \ If not, accept it anyway with probability R(to be determiend by exp(-kt/T), MonteCarlo Annealing
#6: Repeat process for certain amount of epoch until district configuration is optimized
'''


class Precint:
    def __init__(self, name="default", id=0, pop=0, votes=0, party_1=0, party_2=0):
        self.name = name
        self.id = id
        self.pop = pop
        self.votes = votes
        self.party_1 = party_1
        self.party_2 = party_2


class Dict_Trait(enum.Enum):
    name = 0
    id = 1
    pop = 2
    total_votes = 3
    party_1 = 4
    party_2 = 5
    party_3 = 6  # Party 3 is whoever that gets the most votes besides the top 2 parties, independent or other parties
    color = 7


test = Precint("test")


# Implement Graph Partition

# Generates square graph used for testing
def nxn_square_graph_gen(n):
    G = nx.Graph()
    for i in range(n ** 2):
        G.add_node(i)
    edge_list = []
    for j in range(n ** 2 - 1):
        if (j % n) == (n - 1) and j < n * (n - 1):
            edge_list.extend([(j, j + n)])
        elif j >= n * (n - 1):
            edge_list.extend([(j, j + 1)])
        else:
            edge_list.extend([(j, j + 1), (j, j + n)])
    G.add_edges_from(edge_list)
    return G


# Generate nxm rectangle graph(n,m):
# width n, height m
def nxm_rectangle_graph_gen(n, m):
    G = nx.Graph()
    for i in range(n * m):
        G.add_node(i)
    edge_list = []
    for j in range(n * m - 1):
        if (j % n) == (n - 1) and j < n * (m - 1):
            edge_list.extend([(j, j + n)])
        elif j >= n * (m - 1):
            edge_list.extend([(j, j + 1)])
        else:
            edge_list.extend([(j, j + 1), (j, j + n)])
    G.add_edges_from(edge_list)
    return G


# Used to convert adj_list generated by networkx into something pymetis can use to generate partition
def adj_list_to_metislist(adj_list):
    list_temp = []
    for line in adj_list:
        list_ = [int(i) for i in line.split(' ')]
        list_.pop(0)
        list_temp.append(list_)
    return list_temp


# Used to convert adj_lists (which is generator class) from networkx into python lists
def nx_gen_object_to_list(gen_object):
    list_temp = []
    for line in gen_object:
        list_ = [line]
        list_temp.extend(list_)
    return list_temp


def return_adj_list_of_graph(G: nx.Graph()) -> list:
    return_list = []
    for node in G.nodes():
        return_list.append([n for n in G.neighbors(node)])
    return return_list


# Take graph (G) and split it into n partitions return list containing lists of partition nodes
def gen_init_part(G: nx.Graph(), n: int) -> list:
    partition_node_list = []
    adj_list = return_adj_list_of_graph(G)
    n_cuts, membership = pymetis.part_graph(n, adjacency=adj_list)
    print(n_cuts)
    print(membership)
    nodes_part_0 = np.argwhere(np.array(membership) == 0).ravel()
    print(nodes_part_0)
    for i in range(n):
        print(i)
        node_temp_list = []
        node_temp_list = np.argwhere(np.array(membership) == i).ravel()  # taken from
        # \https://github.com/inducer/pymetis#readme
        # print(node_temp_list)
        partition_node_list.append(node_temp_list)
    return partition_node_list


# Take graph (G) and partion node list and return switch one node from one partition to neighboring partition when valid
# select another node randomly if switch turns out to be invalid(i.e. breaks connection of partition)
def random_switch(G: nx.Graph(), partition_node_list: list) -> (list, bool):
    is_switched = False
    is_node_list_changed = False
    return_list = []
    new_switched_partition_node_list = copy.deepcopy(partition_node_list.copy())  # make deep copy of node list
    random_partition_num = random.randint(0, len(partition_node_list) - 1)  # select random partition to switch from
    boundary_edge_list = nx_gen_object_to_list(
        nx.edge_boundary(G, partition_node_list[random_partition_num]))  # boundary edges of partition
    random_boundary_edge_pair_index = random.randint(0,
                                                     len(boundary_edge_list) - 1)  # first node is in current partition num second node is partner
    random_boundary_edge_pair = boundary_edge_list[random_boundary_edge_pair_index]
    # find partner partition to switch to
    partner_partition_num = 0
    print(random_boundary_edge_pair)
    for kth_partition in new_switched_partition_node_list:
        if random_boundary_edge_pair[1] in kth_partition:
            break
        else:
            partner_partition_num = partner_partition_num + 1

    # switch between the two random_boundary_edge_pair nodes
    index_loc_0 = np.where(new_switched_partition_node_list[random_partition_num] == random_boundary_edge_pair[0])
    index_loc_1 = np.where(new_switched_partition_node_list[partner_partition_num] == random_boundary_edge_pair[1])
    new_switched_partition_node_list[random_partition_num][index_loc_0], \
    new_switched_partition_node_list[partner_partition_num][index_loc_1] = \
        new_switched_partition_node_list[partner_partition_num][index_loc_1], \
        new_switched_partition_node_list[random_partition_num][index_loc_0]

    # Check if the new partitions are valided(they should be connected)
    part_0 = G.subgraph(new_switched_partition_node_list[random_partition_num])
    part_1 = G.subgraph(new_switched_partition_node_list[partner_partition_num])
    fst_part_connect_state = nx.is_connected(part_0)
    snd_part_connect_state = nx.is_connected(part_1)
    print(random_boundary_edge_pair[0])
    print(random_boundary_edge_pair[1])
    print(new_switched_partition_node_list[random_partition_num])
    print(new_switched_partition_node_list[partner_partition_num])
    print(part_0)
    print(part_1)
    print('part vs new')
    print(partition_node_list)
    print(new_switched_partition_node_list)
    if np.array_equal(np.array(new_switched_partition_node_list, dtype=object),
                      np.array(partition_node_list, dtype=object)):
        is_node_list_changed = False
    else:
        is_node_list_changed = True
    if (
            fst_part_connect_state and snd_part_connect_state and is_node_list_changed):  # is switch valid and actually happened
        print(fst_part_connect_state)
        print(snd_part_connect_state)
        is_switched = True
        return_list = new_switched_partition_node_list
    else:
        print(fst_part_connect_state)
        print(snd_part_connect_state)
        print(is_node_list_changed)
        is_switched = False
        return_list = partition_node_list
    return return_list, is_switched


# Take graph (G) and partion node list and return eat one node from one neighboring partition to neighboring partition
# when valid
# select another node randomly if eat turns out to be invalid(i.e. breaks connection of partition)
def eat_random_node(G: nx.Graph(), partition_node_list: list) -> (list, bool):
    is_eat_true = False
    is_node_list_changed = False
    return_list = []
    is_proper_partition_picked = False
    new_switched_partition_node_list = copy.deepcopy(partition_node_list.copy())  # make deep copy of node list

    # If partner partition has only one node repeat random picking process, should not eliminate partition altogether
    while True:
        random_partition_num = random.randint(0, len(partition_node_list) - 1)  # select random partition to switch from
        boundary_edge_list = nx_gen_object_to_list(
            nx.edge_boundary(G, partition_node_list[random_partition_num]))  # boundary edges of partition
        random_boundary_edge_pair_index = random.randint(0,
                                                         len(boundary_edge_list) - 1)  # first node is in current partition num second node is partner
        random_boundary_edge_pair = boundary_edge_list[random_boundary_edge_pair_index]
        # find partner partition to eat from
        partner_partition_num = 0
        print(random_boundary_edge_pair)
        # find partner partition number
        for kth_partition in new_switched_partition_node_list:
            if random_boundary_edge_pair[1] in kth_partition:
                break
            else:
                partner_partition_num = partner_partition_num + 1
        if (len(partition_node_list[partner_partition_num]) == 1):
            print("Remaining Node 1 Case Triggered")
            is_proper_partition_picked = False
        else:
            is_proper_partition_picked = True
        if (is_proper_partition_picked == True):
            break
        elif len(partition_node_list[random_partition_num]) == G.number_of_nodes() - (len(partition_node_list) - 1):
            print('Partition ' + str(random_partition_num) + ' has reached max size of ' + str(
                G.number_of_nodes() - (len(partition_node_list) - 1)))
            return partition_node_list, False
        else:
            pass

    # For some reason new_switched_partition_node_list[random_partition_num] is treated as numpy narray
    # Use numpy functions instead of list when operating on this.

    # random_partition_num partition will eat the entirety of boudary edge pair nodes
    # index_loc_0 = np.where(new_switched_partition_node_list[random_partition_num] == random_boundary_edge_pair[0])
    index_loc_1 = np.where(new_switched_partition_node_list[partner_partition_num] == random_boundary_edge_pair[1])
    # delete from partner partition (random_boundary_edge_pair[1])
    new_switched_partition_node_list[partner_partition_num] = np.delete(
        new_switched_partition_node_list[partner_partition_num], index_loc_1)
    # add to random partition
    new_switched_partition_node_list[random_partition_num] = np.append(
        new_switched_partition_node_list[random_partition_num], random_boundary_edge_pair[1])
    # new_switched_partition_node_list[random_partition_num][index_loc_0], new_switched_partition_node_list[partner_partition_num][index_loc_1] = new_switched_partition_node_list[partner_partition_num][index_loc_1], new_switched_partition_node_list[random_partition_num][index_loc_0]

    # Check if the new partitions are valided(they should be connected)
    part_0 = G.subgraph(new_switched_partition_node_list[random_partition_num])
    part_1 = G.subgraph(new_switched_partition_node_list[partner_partition_num])
    fst_part_connect_state = nx.is_connected(part_0)
    snd_part_connect_state = nx.is_connected(part_1)
    print(random_boundary_edge_pair[0])
    print(random_boundary_edge_pair[1])
    print(new_switched_partition_node_list[random_partition_num])
    print(new_switched_partition_node_list[partner_partition_num])
    print(part_0)
    print(part_1)
    print('part vs new')
    print(partition_node_list)
    print(new_switched_partition_node_list)
    if np.array_equal(np.array(new_switched_partition_node_list, dtype=object),
                      np.array(partition_node_list, dtype=object)):
        is_node_list_changed = False
    else:
        is_node_list_changed = True
    if (
            fst_part_connect_state and snd_part_connect_state and is_node_list_changed):  # is switch valid and actually happened
        print(fst_part_connect_state)
        print(snd_part_connect_state)
        is_eat_true = True
        return_list = new_switched_partition_node_list
    else:
        print(fst_part_connect_state)
        print(snd_part_connect_state)
        print(is_node_list_changed)
        is_eat_true = False
        return_list = partition_node_list
    return return_list, is_eat_true


def DEBUG_FUNCTION_feed_partition_0(G: nx.Graph(), partition_node_list: list) -> (list, bool):
    is_eat_true = False
    is_node_list_changed = False
    return_list = []
    is_proper_partition_picked = False
    new_switched_partition_node_list = copy.deepcopy(partition_node_list.copy())  # make deep copy of node list

    # If partner partition has only one node repeat random picking process, should not eliminate partition altogether
    while True:
        # random_partition_num = random.randint(0,len(partition_node_list)-1) # select random partition to switch from
        random_partition_num = 0
        boundary_edge_list = nx_gen_object_to_list(
            nx.edge_boundary(G, partition_node_list[random_partition_num]))  # boundary edges of partition
        random_boundary_edge_pair_index = random.randint(0,
                                                         len(boundary_edge_list) - 1)  # first node is in current partition num second node is partner
        random_boundary_edge_pair = boundary_edge_list[random_boundary_edge_pair_index]
        print(random_boundary_edge_pair)
        # find partner partition to eat from
        partner_partition_num = 0
        # find partner partition number
        for kth_partition in new_switched_partition_node_list:
            if random_boundary_edge_pair[1] in kth_partition:
                break
            else:
                partner_partition_num = partner_partition_num + 1
        if (len(partition_node_list[partner_partition_num]) == 1):
            is_proper_partition_picked = False
        else:
            is_proper_partition_picked = True
        if (is_proper_partition_picked == True):
            break
        elif len(partition_node_list[random_partition_num]) == G.number_of_nodes() - (len(partition_node_list) - 1):
            print('Partition ' + str(random_partition_num) + ' has reached max size of ' + str(
                G.number_of_nodes() - (len(partition_node_list) - 1)))
            return partition_node_list, False
        else:
            pass

    # For some reason new_switched_partition_node_list[random_partition_num] is treated as numpy narray
    # Use numpy functions instead of list when operating on this.

    # random_partition_num partition will eat the entirety of boudary edge pair nodes
    # index_loc_0 = np.where(new_switched_partition_node_list[random_partition_num] == random_boundary_edge_pair[0])
    index_loc_1 = np.where(new_switched_partition_node_list[partner_partition_num] == random_boundary_edge_pair[1])
    # delete from partner partition (random_boundary_edge_pair[1])
    new_switched_partition_node_list[partner_partition_num] = np.delete(
        new_switched_partition_node_list[partner_partition_num], index_loc_1)
    # add to random partition
    new_switched_partition_node_list[random_partition_num] = np.append(
        new_switched_partition_node_list[random_partition_num], random_boundary_edge_pair[1])
    # new_switched_partition_node_list[random_partition_num][index_loc_0], new_switched_partition_node_list[partner_partition_num][index_loc_1] = new_switched_partition_node_list[partner_partition_num][index_loc_1], new_switched_partition_node_list[random_partition_num][index_loc_0]

    # Check if the new partitions are valided(they should be connected)
    part_0 = G.subgraph(new_switched_partition_node_list[random_partition_num])
    part_1 = G.subgraph(new_switched_partition_node_list[partner_partition_num])
    fst_part_connect_state = nx.is_connected(part_0)
    snd_part_connect_state = nx.is_connected(part_1)
    if np.array_equal(np.array(new_switched_partition_node_list, dtype=object),
                      np.array(partition_node_list, dtype=object)):
        is_node_list_changed = False
    else:
        is_node_list_changed = True
    if (
            fst_part_connect_state and snd_part_connect_state and is_node_list_changed):  # is switch valid and actually happened
        is_eat_true = True
        return_list = new_switched_partition_node_list
    else:
        is_eat_true = False
        return_list = partition_node_list
    return return_list, is_eat_true


def print_node_list(node_list):
    for line in node_list:
        print(line)


def get_color_map_from_dict(input_dict):
    output_list = []
    for i in range(len(input_dict)):
        output_list.extend([input_dict[i][Dict_Trait.color]])
    return output_list


# Calculate result of one district add the all the nodes up into tuple form result
# (partition_pop, partition_vote, partition_party_1_vote, partition_party_2_vote, district_winner, wasated_vote
# Output: (part_pop, part_vote, part_party_1_vote, part_party_2_vote, district_winner, wasted_vote)
def calculate_part_result(G: nx.Graph, node_list: list):
    part_pop = 0
    part_vote = 0
    part_party_1_vote = 0
    part_party_2_vote = 0
    part_party_3_vote = 0
    district_winner = 0
    wasted_vote = 0  # wasted vote by party1 is (+) while wasted vote by party2 is (-)
    for node_num in node_list:
        part_pop = part_pop + G.nodes[node_num][Dict_Trait.pop]
        part_vote = part_vote + G.nodes[node_num][Dict_Trait.total_votes]
        part_party_1_vote = part_party_1_vote + G.nodes[node_num][Dict_Trait.party_1]
        part_party_2_vote = part_party_2_vote + G.nodes[node_num][Dict_Trait.party_2]
        part_party_3_vote = part_party_3_vote + G.nodes[node_num][Dict_Trait.party_3]
    if part_party_1_vote > part_party_2_vote and part_party_1_vote > part_party_3_vote:
        district_winner = 1
        if (part_party_1_vote > part_party_2_vote):
            wasted_vote = wasted_vote - part_party_2_vote
    elif part_party_2_vote > part_party_1_vote and part_party_2_vote > part_party_3_vote:
        district_winner = 2
        if (part_party_2_vote > part_party_1_vote):
            wasted_vote = wasted_vote + part_party_1_vote
    elif part_party_3_vote > part_party_2_vote and part_party_3_vote > part_party_1_vote:
        district_winner = 3
    return (part_pop, part_vote, part_party_1_vote, part_party_2_vote, district_winner, wasted_vote)


# Calculate election result of graph with the input partition configuration
# Output Total Population, Total Vote Count, Voting Share of Party1/2 ,Number of Districts Won by Party_1 and Party_2,
# Variation of Population, and Efficiency Gap
def calculate_graph_result(G: nx.Graph(), partition_node_list: list, print_district_by_district_result=False):
    iteration = 0
    graph_pop = 0
    graph_vote = 0
    graph_party_1_vote = 0
    graph_party_2_vote = 0
    party_1_district_won = 0
    party_2_district_won = 0
    party_3_district_won = 0
    pop_avg = 0.
    pop_variance = 0.
    party_1_wasted_vote = 0
    party_2_wasted_vote = 0
    graph_efficiency_gap = 0.  # party_1_wasted_vote-party_2_wasted_vote/graph_vote # (-) favors party1 (+) favors
    # party2
    part_result_list = []
    pop_list = []
    for part_list in partition_node_list:
        part_result_list.append(calculate_part_result(G, part_list))
        if (print_district_by_district_result):
            print('District #', iteration, 'Result')
            print_district_result(*(part_result_list[iteration]))
            print('\n')
            iteration = iteration + 1
    for tuples in part_result_list:
        graph_pop = graph_pop + tuples[0]
        pop_list.append(tuples[0])
        graph_vote = graph_vote + tuples[1]
        graph_party_1_vote = graph_party_1_vote + tuples[2]
        graph_party_2_vote = graph_party_2_vote + tuples[3]
        if (tuples[4] == 1):
            party_1_district_won = party_1_district_won + 1
        elif (tuples[4] == 2):
            party_2_district_won = party_2_district_won + 1
        elif (tuples[4] == 3):
            party_3_district_won = party_3_district_won + 1

        if (tuples[5] > 0):
            party_1_wasted_vote = party_1_wasted_vote + tuples[5]
        elif (tuples[5] < 0):
            party_2_wasted_vote = party_2_wasted_vote + abs(tuples[5])

    pop_avg = statistics.mean(pop_list)
    pop_variance = statistics.variance(pop_list)
    graph_efficiency_gap = ((party_1_wasted_vote - party_2_wasted_vote) / graph_vote) * 100  # percentage
    return (graph_pop, graph_vote, graph_party_1_vote, graph_party_2_vote, party_1_district_won, party_2_district_won,
            party_3_district_won, pop_avg, pop_variance, party_1_wasted_vote, party_2_wasted_vote, graph_efficiency_gap)


def print_district_result(part_pop, part_vote, part_party_1_vote, part_party_2_vote, district_winner, wasted_vote):
    percentage1 = (part_party_1_vote / part_vote) * 100
    percentage2 = (part_party_2_vote / part_vote) * 100
    print('District Result')
    print('Total District Population: ', part_pop)
    print('Total Vote: ', part_vote)
    print('Total Party1 Vote: ', part_party_1_vote, ' (', percentage1, '%)')
    print('Total Party2 Vote: ', part_party_2_vote, ' (', percentage2, '%)')
    print('District Winner: ', district_winner)
    print('Wasted Votes: ', wasted_vote)


def print_graph_result(graph_pop, graph_vote, graph_party_1_vote, graph_party_2_vote, party_1_district_won,
                       party_2_district_won, party_3_district_won, pop_avg, pop_variance, party_1_wasted_vote,
                       party_2_wasted_vote, graph_efficiency_gap):
    percentage1 = (graph_party_1_vote / graph_vote) * 100
    percentage2 = (graph_party_2_vote / graph_vote) * 100
    print('Graph(Province) Result')
    print('Total District Population: ', graph_pop)
    print('Average District Population: ', pop_avg)
    print('Variance of District Population: ', pop_variance)
    print('Total Vote: ', graph_vote)
    print('Total Party1 Vote: ', graph_party_1_vote, ' (', percentage1, '%)')
    print('Total Party2 Vote: ', graph_party_2_vote, ' (', percentage2, '%)')
    print('Party1 Districts: ', party_1_district_won)
    print('Party2 Districts: ', party_2_district_won)
    print('Party3 Districts: ', party_3_district_won)
    print('Party1 Wasted Votes: ', party_1_wasted_vote)
    print('Party2 Wasted Votes: ', party_2_wasted_vote)
    print('Efficiency Gap: ', graph_efficiency_gap, '(%) (Negative values favor Party1 while positive values favor '
                                                    'Party2.)')


print(type(Dict_Trait.name))
Dict_format = dict(
    {'name': 'default', 'id': 0, 'pop': 0, 'total_votes': 0, 'party_1': 0, 'party_2': 0, 'color': 'white'})
Dict_example = dict(
    {Dict_Trait.name: 'default', Dict_Trait.id: 0, Dict_Trait.pop: 0, Dict_Trait.total_votes: 0, Dict_Trait.party_1: 0,
     Dict_Trait.party_2: 0, Dict_Trait.party_3: 0, Dict_Trait.color: 'white'})

key_list = []
n = 5
m = 10
G = nxm_rectangle_graph_gen(n, m)
for x in range(G.number_of_nodes()):
    key_list.append(x)

value_list = []
for i in range(G.number_of_nodes()):
    dict_element_1 = {Dict_Trait.name: 'default', Dict_Trait.id: 0, Dict_Trait.pop: 10, Dict_Trait.total_votes: 10,
                      Dict_Trait.party_1: 10, Dict_Trait.party_2: 0, Dict_Trait.party_3: 0, Dict_Trait.color: 'blue'}
    dict_element_2 = {Dict_Trait.name: 'default', Dict_Trait.id: 0, Dict_Trait.pop: 10, Dict_Trait.total_votes: 10,
                      Dict_Trait.party_1: 0, Dict_Trait.party_2: 10, Dict_Trait.party_3: 0, Dict_Trait.color: 'yellow'}
    if i % n > 1:
        dict_element_1[Dict_Trait.id] = i
        value_list.append(dict_element_1)
    else:
        dict_element_2[Dict_Trait.id] = i
        value_list.append(dict_element_2)

node_dict = {key_list[i]: value_list[i] for i in range(len(key_list))}
print(node_dict)
print((node_dict[0]))
print((node_dict[1]))
print((node_dict[2]))
print((node_dict[3]))
print((node_dict[4]))
nx.set_node_attributes(G, node_dict)

# layout = nx.planar_layout(G)
color_map = get_color_map_from_dict(node_dict)
print(color_map)
nx.draw(G, with_labels=True, node_color=color_map)
plt.show()
print_district_result(*(calculate_part_result(G, [0, 1, 2, 3, 4])))
partition_node_list = gen_init_part(G, 5)
print_node_list(partition_node_list)
print_graph_result(*(calculate_graph_result(G, partition_node_list, True)))

# Test configuration taken from (https://en.wikipedia.org/wiki/Gerrymandering#/media/File:DifferingApportionment.svg)
config1 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
           [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
           [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
           [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
           [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]]
config2 = [[0, 5, 6, 7, 8, 10, 11, 12, 13, 15],
           [16, 17, 18, 20, 21, 25, 26, 31, 32, 33],
           [30, 35, 36, 37, 38, 40, 41, 42, 43, 45],
           [1, 2, 3, 4, 9, 14, 19, 24, 23, 22],
           [27, 28, 29, 34, 39, 44, 46, 47, 48, 49]]
config3 = [[0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
           [1, 6, 11, 16, 21, 26, 31, 36, 41, 46],
           [2, 7, 12, 17, 22, 27, 32, 37, 42, 47],
           [3, 8, 13, 18, 23, 28, 33, 38, 43, 48],
           [4, 9, 14, 19, 24, 29, 34, 39, 44, 49]]
config4 = [[0, 1, 2, 3, 4, 7, 8, 9, 13, 14],
           [5, 6, 10, 11, 12, 15, 16, 17, 18, 19],
           [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
           [30, 31, 32, 33, 34, 37, 38, 39, 43, 44],
           [35, 36, 40, 41, 42, 45, 46, 47, 48, 49]]
print('\nConfig1\n')
print_graph_result(*(calculate_graph_result(G, config1, print_district_by_district_result=False)))
print('\nConfig2\n')
print_graph_result(*(calculate_graph_result(G, config2, print_district_by_district_result=False)))
print('\nConfig3\n')
print_graph_result(*(calculate_graph_result(G, config3, print_district_by_district_result=False)))
print('\nConfig4\n')
print_graph_result(*(calculate_graph_result(G, config4, print_district_by_district_result=False)))

config1_test = list(set().union(config1[0], config1[1], config1[2], config1[3], config1[4]))
config2_test = list(set().union(config2[0], config2[1], config2[2], config2[3], config2[4]))
config3_test = list(set().union(config3[0], config3[1], config3[2], config3[3], config3[4]))
config4_test = list(set().union(config4[0], config4[1], config4[2], config4[3], config4[4]))
print(config1_test)
print(config2_test)
print(config3_test)
print(config4_test)
print(len(config1_test),
      len(config2_test),
      len(config3_test),
      len(config4_test))
# G.add_nodes_from([(0,{})])
# nx.set_node_attributes(G,Dict_format)


'''
n = 5
part_num = 3
#G = nxn_square_graph_gen(n)
G = nx.complete_graph(20)
H = nxn_square_graph_gen(n)
partition_node_list = gen_init_part(G, part_num)
print("Original Partition")
print_node_list(partition_node_list)
new_list,state = eat_random_node(G, partition_node_list)
print("New Partition")
print_node_list(new_list)

print("Square Graph")
partition_node_list = gen_init_part(H, part_num)
print("Original Partition")
print_node_list(partition_node_list)
new_list,state = eat_random_node(H, partition_node_list)
print("New Partition")
print_node_list(new_list)
print(state)

'''

'''
new_list,state = random_switch(G, partition_node_list)
new_list,state = random_switch(G, new_list)
new_list,state = random_switch(G, new_list)
new_list,state = random_switch(G, new_list)
print_node_list(partition_node_list)
print_node_list(new_list)

fig = nx.draw(G,with_labels=True)

sub_graph_0 = G.subgraph(partition_node_list[0])
sub_graph_1 = G.subgraph(partition_node_list[1])
sub_graph_2 = G.subgraph(partition_node_list[2])
nx.draw(sub_graph_0, with_labels=True)
nx.draw(sub_graph_1, with_labels=True)
nx.draw(sub_graph_2, with_labels=True)

sub_graph_0_ = G.subgraph(new_list[0])
sub_graph_1_ = G.subgraph(new_list[1])
sub_graph_2_ = G.subgraph(new_list[2])

nx.draw(sub_graph_0_, with_labels=True)
nx.draw(sub_graph_1_, with_labels=True)
nx.draw(sub_graph_2_, with_labels=True)


plt.show()
'''

#print(state)



'''
H = nxn_square_graph_gen(5)


adj_list = nx.generate_adjlist(H)

t = adj_list_to_metislist(adj_list)


n_cuts, membership = pymetis.part_graph(2, adjacency=t)
nodes_part_0 = np.argwhere(np.array(membership) == 0).ravel() # [3, 5, 6]
nodes_part_1 = np.argwhere(np.array(membership) == 1).ravel() # [0, 1, 2, 4]

nodes_part_0 = np.argwhere(np.array(membership) == 0).ravel() # [3, 5, 6]
nodes_part_1 = np.argwhere(np.array(membership) == 1).ravel() # [0, 1, 2, 4]
H_0 = H.subgraph(nodes_part_0)

nx.draw(H_0,with_labels=True)

plt.show()
H_0_boundary = nx.edge_boundary(H,nodes_part_0)
print(nx_gen_object_to_list(H_0_boundary))

H_1 = H.subgraph(nodes_part_1)
nx.draw(H_1, with_labels=True)
plt.show()
H_1_boundary = nx.edge_boundary(H,nodes_part_1)
print(nx_gen_object_to_list(H_1_boundary))

# nx.read_shp('emd.shp')
'''