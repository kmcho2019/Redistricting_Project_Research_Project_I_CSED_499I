import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
import pymetis
import numpy as np
import random
import copy
import enum
import statistics
import math

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
    nodes_part_0 = np.argwhere(np.array(membership) == 0).ravel()
    for i in range(n):
        node_temp_list = []
        node_temp_list = np.argwhere(np.array(membership) == i).ravel()  # taken from
        # \https://github.com/inducer/pymetis#readme
        # print(node_temp_list)
        partition_node_list.append(node_temp_list)
    return partition_node_list

# Take graph (G) and split it into n partitions return list containing lists of partition nodes
# Must be used when adj_list index does not match node number.
# gen_init_part simply assumes that node number corresponds with adj_list.
# pymetis.part_graph requires that adjacency[i] it is an iterable
# of vertices adjacent to vertex i.
# In cases where this cannot be guaranteed it must be converted first to 0,1, ...
# Then be converted back to original format
def alt_gen_init_part(G: nx.Graph(), n: int) -> list:
    partition_node_list = []
    replacement_dict = {}
    input_node_list = list(G.nodes())
    restore_node_num_dict = {idx: x for idx,x in enumerate(input_node_list)}
    encode_node_num_dict = {x : idx for idx,x in enumerate(input_node_list)}
    adj_list = return_adj_list_of_graph(G)
    print(adj_list)
    print(type(adj_list))
    print(restore_node_num_dict)
    print(encode_node_num_dict)
    l = []
    for x in adj_list:
        l.append([encode_node_num_dict.get(n) for n in x])
    adj_list = l
    #n_cuts, membership = pymetis.part_graph(n, adjacency=adj_list) #need to fix as it results in non-contigous partitions
    n_cuts, membership = pymetis.part_graph(n, adjacency=adj_list,options=pymetis.Options(contig=True)) #unusable due to old version of pymetis being installed
    nodes_part_0 = np.argwhere(np.array(membership) == 0).ravel()
    for i in range(n):
        node_temp_list = []
        node_temp_list = np.argwhere(np.array(membership) == i).ravel()  # taken from
        # \https://github.com/inducer/pymetis#readme
        # print(node_temp_list)
        partition_node_list.append(node_temp_list)
    temp = []
    for x in partition_node_list:
        temp.append([restore_node_num_dict.get(n) for n in x])
    partition_node_list = temp
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
    if np.array_equal(np.array(new_switched_partition_node_list, dtype=object),
                      np.array(partition_node_list, dtype=object)):
        is_node_list_changed = False
    else:
        is_node_list_changed = True
    if (
            fst_part_connect_state and snd_part_connect_state and is_node_list_changed):  # is switch valid and actually happened
        is_switched = True
        return_list = new_switched_partition_node_list
    else:
        is_switched = False
        return_list = partition_node_list
    return return_list, is_switched


# Take graph (G) and partion node list and return eat one node from one neighboring partition to neighboring partition
# when valid
# select another node randomly if eat turns out to be invalid(i.e. breaks connection of partition)
def eat_random_node(G: nx.Graph(), partition_node_list: list, debug_print_mode = False) -> (list, bool):
    if debug_print_mode:
        print('\n\n')
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

    #check if total len number remains constant
    random_part_original_len = len(new_switched_partition_node_list[random_partition_num])
    partner_part_original_len = len(new_switched_partition_node_list[partner_partition_num])
    # For some reason new_switched_partition_node_list[random_partition_num] is treated as numpy narray
    #print('Type;!')
    #print(type(new_switched_partition_node_list[random_partition_num]))
    # Use numpy functions instead of list when operating on this.
    if debug_print_mode:
        print('Boundary Edge: ', random_boundary_edge_pair)
        print('Original Random Partition: ', new_switched_partition_node_list[random_partition_num])
        print('Original Partner Partition: ', new_switched_partition_node_list[partner_partition_num])
        print('Partition Numbers (Random, Partner)', random_partition_num,partner_partition_num)
    # random_partition_num partition will eat the entirety of boundary edge pair nodes
    # index_loc_0 = np.where(new_switched_partition_node_list[random_partition_num] == random_boundary_edge_pair[0])
    index_loc_1 = np.where(new_switched_partition_node_list[partner_partition_num] == random_boundary_edge_pair[1])
    if debug_print_mode:
        print(index_loc_1)
    index_loc_1 = 0
    for ele in new_switched_partition_node_list[partner_partition_num]:
        if ele == random_boundary_edge_pair[1]:
            break
        else:
            index_loc_1 = index_loc_1 + 1

    if debug_print_mode:
        print(index_loc_1)
        print('Index Number of Edge Node in Partner Partition: ', index_loc_1)
    #print(len(index_loc_1))
    # delete from partner partition (random_boundary_edge_pair[1])
    new_switched_partition_node_list[partner_partition_num] = np.delete(
        new_switched_partition_node_list[partner_partition_num], index_loc_1)
    # add to random partition
    new_switched_partition_node_list[random_partition_num] = np.append(
        new_switched_partition_node_list[random_partition_num], random_boundary_edge_pair[1])
    # new_switched_partition_node_list[random_partition_num][index_loc_0], new_switched_partition_node_list[partner_partition_num][index_loc_1] = new_switched_partition_node_list[partner_partition_num][index_loc_1], new_switched_partition_node_list[random_partition_num][index_loc_0]
    if debug_print_mode:
        print('New Random Partition: ', new_switched_partition_node_list[random_partition_num])
        print('New Partner Partition: ', new_switched_partition_node_list[partner_partition_num])
    # Check if the new partitions are valid(they should be connected)
    part_0 = G.subgraph(new_switched_partition_node_list[random_partition_num])
    part_1 = G.subgraph(new_switched_partition_node_list[partner_partition_num])
    fst_part_connect_state = nx.is_connected(part_0)
    snd_part_connect_state = nx.is_connected(part_1)
    # Is length maintained?
    new_random_part_len = len(new_switched_partition_node_list[random_partition_num])
    new_partner_part_len = len(new_switched_partition_node_list[partner_partition_num])
    if debug_print_mode:
        print('Original Random Part Length: ', random_part_original_len)
        print('Original Partner Part Length: ', partner_part_original_len)
        print('New Random Part Length: ', new_random_part_len)
        print('New Partner Part Length: ', new_partner_part_len)
    if(new_random_part_len + new_partner_part_len == random_part_original_len + partner_part_original_len):
        is_len_valid = True
    else:
        is_len_valid = False
    new_switched_partition_node_list[random_partition_num].sort()
    new_switched_partition_node_list[partner_partition_num].sort()
    if np.array_equal(np.array(new_switched_partition_node_list, dtype=object),
                      np.array(partition_node_list, dtype=object)):
        is_node_list_changed = False
    else:
        is_node_list_changed = True
    if (fst_part_connect_state and snd_part_connect_state and is_node_list_changed and is_len_valid):  # is eating valid and actually happened
        is_eat_true = True
        return_list = new_switched_partition_node_list
    else:
        is_eat_true = False
        return_list = partition_node_list

    if debug_print_mode:
        if(is_eat_true):
            print('Eat Valid')
        else:
            print('Eat Invalid')
            print('1st Connect, 2nd Connect, List Change, Length Validity:', fst_part_connect_state, snd_part_connect_state, is_node_list_changed, is_len_valid)
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
# Output: (part_pop, part_vote, part_party_1_vote, part_party_2_vote, district_winner, party_1_wasted_vote, party_2_wasted_vote)
def calculate_part_result(G: nx.Graph, node_list: list):
    part_pop = 0
    part_vote = 0
    part_party_1_vote = 0
    part_party_2_vote = 0
    part_party_3_vote = 0
    district_winner = 0
    #wasted_vote = 0  # wasted vote by party1 is (+) while wasted vote by party2 is (-)
    party_1_wasted_vote = 0
    party_2_wasted_vote = 0
    for node_num in node_list:
        part_pop = part_pop + G.nodes[node_num][Dict_Trait.pop]
        part_vote = part_vote + G.nodes[node_num][Dict_Trait.total_votes]
        part_party_1_vote = part_party_1_vote + G.nodes[node_num][Dict_Trait.party_1]
        part_party_2_vote = part_party_2_vote + G.nodes[node_num][Dict_Trait.party_2]
        part_party_3_vote = part_party_3_vote + G.nodes[node_num][Dict_Trait.party_3]
    if part_party_1_vote > part_party_2_vote and part_party_1_vote > part_party_3_vote:
        district_winner = 1
        party_1_wasted_vote = max(part_party_1_vote-(int(part_vote/2)+1),0)
        party_2_wasted_vote = part_party_2_vote
        #wasted_vote = wasted_vote - part_party_2_vote
    elif part_party_2_vote > part_party_1_vote and part_party_2_vote > part_party_3_vote:
        district_winner = 2
        party_2_wasted_vote = max(part_party_2_vote-(int(part_vote/2)+1),0)
        party_1_wasted_vote = part_party_1_vote
        #wasted_vote = wasted_vote + part_party_1_vote
    elif part_party_3_vote > part_party_2_vote and part_party_3_vote > part_party_1_vote:
        district_winner = 3
        party_1_wasted_vote = part_party_1_vote
        party_2_wasted_vote = part_party_2_vote

    return (part_pop, part_vote, part_party_1_vote, part_party_2_vote, district_winner, party_1_wasted_vote, party_2_wasted_vote)


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
    tied_districts = 0
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
        else:
            print('Ties')
            tied_districts = tied_districts + 1
            print(tuples)

        party_1_wasted_vote = party_1_wasted_vote + tuples[5]
        party_2_wasted_vote = party_2_wasted_vote + tuples[6]



    pop_avg = statistics.mean(pop_list)
    pop_variance = statistics.variance(pop_list)
    graph_efficiency_gap = ((party_1_wasted_vote - party_2_wasted_vote) / graph_vote) * 100  # percentage
    return (graph_pop, graph_vote, graph_party_1_vote, graph_party_2_vote, party_1_district_won, party_2_district_won,
            party_3_district_won, pop_avg, pop_variance, party_1_wasted_vote, party_2_wasted_vote, graph_efficiency_gap,tied_districts)


def print_district_result(part_pop, part_vote, part_party_1_vote, part_party_2_vote, district_winner, party_1_wasted_vote, party_2_wasted_vote):
    percentage1 = (part_party_1_vote / part_vote) * 100
    percentage2 = (part_party_2_vote / part_vote) * 100
    print('District Result')
    print('Total District Population: ', part_pop)
    print('Total Vote: ', part_vote)
    print('Total Party1 Vote: ', part_party_1_vote, ' (', percentage1, '%)')
    print('Total Party2 Vote: ', part_party_2_vote, ' (', percentage2, '%)')
    print('District Winner: ', district_winner)
    print('Party 1 Wasted Votes: ', party_1_wasted_vote)
    print('Party 2 Wasted Votes: ', party_2_wasted_vote)


def print_graph_result(graph_pop, graph_vote, graph_party_1_vote, graph_party_2_vote, party_1_district_won,
                       party_2_district_won, party_3_district_won, pop_avg, pop_variance, party_1_wasted_vote,
                       party_2_wasted_vote, graph_efficiency_gap,tied_districts):
    percentage1 = (graph_party_1_vote / graph_vote) * 100
    percentage2 = (graph_party_2_vote / graph_vote) * 100
    print('Graph(Province) Result')
    print('Total Graph(Province) Population: ', graph_pop)
    print('Average Graph(Province) Population: ', pop_avg)
    print('Variance of Graph(Province) Population: ', pop_variance)
    print('Total Vote: ', graph_vote)
    print('Total Party1 Vote: ', graph_party_1_vote, ' (', percentage1, '%)')
    print('Total Party2 Vote: ', graph_party_2_vote, ' (', percentage2, '%)')
    print('Party1 Districts: ', party_1_district_won)
    print('Party2 Districts: ', party_2_district_won)
    print('Party3 Districts: ', party_3_district_won)
    print('Tied Districts: ', tied_districts)
    print('Party1 Wasted Votes: ', party_1_wasted_vote)
    print('Party2 Wasted Votes: ', party_2_wasted_vote)
    print('Efficiency Gap: ', graph_efficiency_gap, '(%) (Negative values favor Party1 while positive values favor '
                                                    'Party2.)')


# Run eat_random_node() to generate next state and compare between current and next states.
# If computed score is better adopt next state if not only adopt with probability of exp(score_diff/Temp)
# Output either input list(if no change) or changed list
# Use for Monte CArlo Simulated Annealing Algorithm
def anneal_step(G: nx.Graph(), current_part_state: list, current_state_score: float, current_temp: float, verbose =False):
    next_part_state,eat_validity = eat_random_node(G, current_part_state)
    next_state_score = compute_state_score(G, next_part_state)
    score_delta = next_state_score - current_state_score

    if(score_delta > 0): #next state is improvement
        output_state = next_part_state
        output_score = next_state_score
        probability = 1. # 1 as it always switches when there is an improvement
        if verbose:
            print('\n')
            print('State Improved')
            print('Temperature: ', current_temp)
            print('Current Score: ', current_state_score)
            print('Next Score: ', next_state_score)
            print('\n')
    else: #next state is not an improvement
        probability = math.exp(score_delta/current_temp)
        if(random.random() <probability): #move to next state even if it is worst under probability
            output_state = next_part_state
            output_score = next_state_score
            if verbose:
                print('\n')
                print('State Not Improved Move Anyway', probability)
                print('Temperature: ', current_temp)
                print('Current Score: ', current_state_score)
                print('Next Score: ', next_state_score)
                print('Probability: ', probability)
                print('\n')
        else:
            output_state = current_part_state
            output_score = current_state_score
            if verbose:
                print('\n')
                print('State Not Improved Do Not Move')
                print('Temperature: ', current_temp)
                print('Current Score: ', current_state_score)
                print('Next Score: ', next_state_score)
                print('Probability: ', probability)
                print('\n')
    return output_state,output_score, probability

def compute_state_score(G: nx.Graph(), state_part_list: list, pop_distribute_weight = 0.8) -> float:
    (efficiency_gap ,pop_variance) = (0,0)
    (_, _, _, _, _, _, _, pop_avg, pop_variance, _, _, graph_efficiency_gap,_) = calculate_graph_result(G,state_part_list)
    pop_portion = 100*(1-math.exp(-(pop_variance/(9*pop_avg)))) * pop_distribute_weight
    partisan_portion = efficiency_gap * (1-pop_distribute_weight)
    val = 5000*math.exp(-0.131*(pop_portion+partisan_portion))
    #val = max((pop_variance + abs(graph_efficiency_gap)),0.1) #simple placeholder function
    #val = 100/val
    return val

def graph_simulated_annealing(G: nx.Graph(), partition_node_list, step_size = 100, verbose = False):
    result_list = []
    initial_score = compute_state_score(G,partition_node_list)
    start_temp = 10000 # Temperature always starts at 10000
    epoch_num = int(start_temp/step_size)
    # temp function Temp = 1000/(time^alpha + 1) (T:10000 ->0.01 as time goes on)
    alpha = 6/(math.log10(epoch_num))
    score_history_list = []
    probability_history_list = []
    result_list,score, probability = anneal_step(G,partition_node_list,initial_score,start_temp, verbose)
    score_history_list.append(score)
    probability_history_list.append(probability)
    for time in range(epoch_num):
        current_temp = start_temp/((time**alpha) + 1)
        result_list, score, probability = anneal_step(G, result_list, score, current_temp, verbose)
        score_history_list.append(score)
        probability_history_list.append(probability)
        #result_list,score, probability = anneal_step(G, result_list, score,start_temp-step_size*time, verbose)
    return result_list,score_history_list, probability_history_list

Dict_format = dict(
    {'name': 'default', 'id': 0, 'pop': 0, 'total_votes': 0, 'party_1': 0, 'party_2': 0, 'color': 'white'})
Dict_example = dict(
    {Dict_Trait.name: 'default', Dict_Trait.id: 0, Dict_Trait.pop: 0, Dict_Trait.total_votes: 0, Dict_Trait.party_1: 0,
     Dict_Trait.party_2: 0, Dict_Trait.party_3: 0, Dict_Trait.color: 'white'})


