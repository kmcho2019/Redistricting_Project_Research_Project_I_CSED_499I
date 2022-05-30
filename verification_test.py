import networkx as nx

from main import*
import pandas as pd

edge_list = [
    (0,1),
    (1,2),
    (2,3),
    (7,6),
    (6,5),
    (5,4),
    (8,9),
    (9,10),
    (10,11),
    (12,13),
    (13,14),
    (14,15),
    (0,8),
    (8,12),
    (7,12),
    (7,0),
    (1,9),
    (9,13),
    (6,13),
    (6,1),
    (2,10),
    (10,14),
    (5,14),
    (5,2),
    (3,11),
    (11,15),
    (4,15),
    (4,3)
]
print(len(edge_list))

G = nx.Graph()
G.add_edges_from(edge_list)
print(nx.check_planarity(G,False))

fixed1_pop = [2673,2071,2043,869,789,756,539,260]
fixed1_party1 = [1008,737,705,645,425,264,126,90]

fixed2_pop = [1839,1732,1671,1406,1050,924,841,537]
fixed2_party2 = [974,799,552,495,423,289,257,211]

#fixed1_party2 = [fixed1_pop[x]-fixed1_party1[x] for x in range(len(fixed1_pop))]
fixed1_party2 = [x-y for x,y in zip(fixed1_pop,fixed1_party1)]
fixed2_party1 = [x-y for x,y in zip(fixed2_pop,fixed2_party2)]

print('fixed1_pop sum: ', sum(fixed1_pop))
print('fixed2_pop sum: ', sum(fixed2_pop))
print('fixed1_party1: ', sum(fixed1_party1))
print('fixed1_party2: ', sum(fixed1_party2))
print('fixed2_party2: ', sum(fixed2_party2))
print('fixed2_party1: ', sum(fixed2_party1))
Dict_format = dict(
    {'name': 'default', 'id': 0, 'pop': 0, 'total_votes': 0, 'party_1': 0, 'party_2': 0, 'color': 'white'})

key_list = [x for x in range(16)]
value_list = [dict(
    {Dict_Trait.name: str(i), Dict_Trait.id: i, Dict_Trait.pop: (fixed1_pop[i]*2 if i < 8 else 2*fixed2_pop[i-8]),
     Dict_Trait.total_votes: (fixed1_pop[i] if i < 8 else fixed2_pop[i-8]), Dict_Trait.party_1: (fixed1_party1[i] if i < 8 else fixed2_party1[i-8]),
     Dict_Trait.party_2: (fixed1_party2[i] if i < 8 else fixed2_party2[i-8]),
     Dict_Trait.party_3: 0, Dict_Trait.color: ('blue' if i < 8 else 'red')})
    for i in range(16)
    ]
verification_dict ={k: v for k,v in zip(key_list,value_list)}
print(len(verification_dict))
#color_map = get_color_map_from_dict(verification_dict)
print(verification_dict)
nx.set_node_attributes(G, verification_dict)
init_part = alt_gen_init_part(G,2)


result_list, log_list = graph_simulated_annealing(G, init_part, 10, False)
compare_before_after_graph_anneal(G, init_part, result_list)
score_history_list = log_list[0]
probability_history_list = log_list[1]
min_score_list = log_list[2]

compare_before_after_graph_anneal(G, init_part, min_score_list[1])

print(init_part)

score_fig = plt.figure(1)
plt.plot(score_history_list)
plt.savefig('verification_score_history.png')
plt.close(score_fig)
prob_fig = plt.figure(2)
plt.plot(probability_history_list)
plt.savefig('verification_prob_history.png')
plt.close(prob_fig)
print(score_history_list)


nx.draw_planar(G,  with_labels=True)
plt.savefig('verification_graph.png')
plt.close()

#init_part_color_map = [dict((init_part[0][i]): 'blue' if i< 8 else (init_part[1][i-8]): 'red') for i in range(16)]
#init partition color
for i in range(16):
    if i in init_part[0]:
        G.nodes[i]['color'] = 0
    else:
        G.nodes[i]['color'] = 1

color_state_map = {0: 'blue', 1: 'red'}
nx.draw_planar(G, node_color=[color_state_map[node[1]['color']] for node in G.nodes(data=True)], with_labels=True)
plt.savefig('verification_init_part_graph.png')
plt.close()

#min partition color
for i in range(16):
    if i in min_score_list[1][0]:
        G.nodes[i]['color'] = 0
    else:
        G.nodes[i]['color'] = 1
nx.draw_planar(G, node_color=[color_state_map[node[1]['color']] for node in G.nodes(data=True)], with_labels=True)
plt.savefig('verification_min_part_graph.png')
plt.close()
generate_log_file('verification_test_log.txt', init_part,result_list,score_history_list,min_score_list)


#########################
#Checking all possible permutations

#converts integers organized in binary format to graph partitions
#operates on 16 nodes or 16 bits
# 2^0 corresponds to node 0 status, 2^1 corresponds to node 1 status, ... 2^15 corresponds to node 15 status
# 0 indicates that the node belongs to partition 0, 1 indicates that the node belongs to partition 1
def binary_to_graph_partition(binary_gray_codes: int):
    l = [[],[]] # 0th list-> partition 0, 1th list-> partition 1
    for i in range(16):
        if (binary_gray_codes // (10 ** i)) % 10 == 0:
            l[0].append(i)
        else:
            l[1].append(i)
    return l

#Accept two partitions of graph G and return True if both partitions are contiguity else return False
def check_contiguity_of_part(G:nx.Graph(), part_list):
    if len(part_list[0]) == 0 or len(part_list[1]) == 0: #consider any empty subgraph as being uncontiguous
        return False
    else:
        part0 = G.subgraph(part_list[0])
        part1 = G.subgraph(part_list[1])
        if nx.is_connected(part0) and nx.is_connected(part1):
            return True
        else:
            return False


gray_code = pd.read_csv('Gray code.csv')
print(gray_code)
print(gray_code.info())
# 16 bit, contiguity, score
gray_code = gray_code.assign(contiguity = bool(0))
gray_code = gray_code.assign(score = 0.)
print(gray_code.info())
data_array = gray_code.to_numpy()
print(data_array)
for config in data_array:
    partition_list = binary_to_graph_partition(config[2])
    #print(partition_list)
    config[3] = check_contiguity_of_part(G,partition_list)
    if config[3]:
        config[4] = compute_state_score(G, partition_list)
    else:
        config[4] = 1.0 # score set to max value because it does not exist
gray_array = data_array[:,[2]]
contiguity_array = data_array[:,[3]]
score_array = data_array[:,[4]]
print('Total number of False in contiguity_array: ', (contiguity_array == False).sum())
print('Total number of 0.0 in score_array: ', (score_array == 0.0).sum())
gray_array = [x[0] for x in gray_array]
contiguity_array = [x[0] for x in contiguity_array]
score_array = [x[0] for x in score_array]
plt.plot(score_array)
plt.savefig('verification_complete_score_curve.png')
plt.close()

#plt.yscale('log')
#plt.plot(score_array)
#plt.show()

#print(data_array)
#print(gray_array)
#print(contiguity_array)
#print(score_array)

output_df =pd.DataFrame(data_array, columns=['dec','bin','gray','contiguity','score'])
print(output_df)
output_df.to_csv('Complete_Graph_Permutation_Score_Computed.csv', index=False)

contig_df = output_df.drop(output_df[output_df.contiguity == False].index)
print(contig_df)
contig_df.to_csv('Contiguous_Graph_Score.csv')
