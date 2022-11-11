import networkx as nx

from main import *
import pandas as pd

partition_number = 7
region_name = 'Daejeon'
iter_per_epoch = 200#100

Dict_format = dict(
    {'name': 'default', 'id': 0, 'pop': 0, 'total_votes': 0, 'party_1': 0, 'party_2': 0, 'color': 'white'})

file_name = r'Daejeon_admin_district_attributes_vba_macro.xlsm'

dfs = pd.read_excel(file_name, sheet_name='adjacency_list')#,encoding=sys.getfilesystemencoding())
dfs.head()
print(dfs.head())
name_head = dfs['ADM_DR_NM']
id_head = dfs['actual_admin_code']
pop_head = dfs['population']
total_vote_head = dfs['Total Vote']
party1_vote_head = dfs['Party 1 Vote']
party2_vote_head = dfs['Party 2 Vote']
party3_vote_head = dfs['Party 3 Vote']

adj_list_head = dfs['admin_neighbor']

print(adj_list_head.iloc[1])




node_num = 0
for x in dfs['ADM_DR_CD'].iloc:
    #print(x)
    if x > 0:
        node_num = node_num + 1
print(node_num)

edge_list = []

name_list = []
id_list = []
pop_list = []
total_vote_list = []
party1_vote_list = []
party2_vote_list = []
party3_vote_list = []



for i in range(node_num):
    neighbor_str = adj_list_head[i]
    str_list = neighbor_str.split(',')
    node_num_list = [int(x) for x in str_list]
    for j in range(len(node_num_list)):
        edge_list.append((int(id_head.iloc[i]), node_num_list[j]))
    name_list.append(name_head.iloc[i])
    id_list.append(int(id_head.iloc[i]))
    pop_list.append(int(pop_head.iloc[i]))
    total_vote_list.append(int(total_vote_head.iloc[i]))
    party1_vote_list.append(int(party1_vote_head.iloc[i]))
    party2_vote_list.append(int(party2_vote_head.iloc[i]))
    party3_vote_list.append(int(party3_vote_head.iloc[i]))


print(adj_list_head[2])

G = nx.Graph()
G.add_edges_from(edge_list)
#remove selfloops as adj_list includes them
G.remove_edges_from(nx.selfloop_edges(G))
print(G.edges())
print(len(G.nodes()))

#generate attribute dictionary
sejong_3611011200 =dict({Dict_Trait.name: '고운동', Dict_Trait.id: 3611011200, Dict_Trait.pop: 34104, Dict_Trait.total_votes: 15230, Dict_Trait.party_1: 8489, Dict_Trait.party_2: 6058, Dict_Trait.party_3: 452, Dict_Trait.color: 'white'})
attribute_list = []
for i in range(node_num):
    attribute_list.append(dict({Dict_Trait.name: name_list[i], Dict_Trait.id: id_list[i], Dict_Trait.pop: pop_list[i], Dict_Trait.total_votes: total_vote_list[i], Dict_Trait.party_1: party1_vote_list[i], Dict_Trait.party_2: party2_vote_list[i], Dict_Trait.party_3: party3_vote_list[i], Dict_Trait.color: 'white'}))

Graph_attribute_dict = {id_list[i]: attribute_list[i] for i in range(len(id_list))}

nx.set_node_attributes(G,Graph_attribute_dict)
nx.draw(G)
plt.savefig(region_name+'_initial_graph.png')
plt.close()
# print('Is G planar?\n',nx.is_planar(G))


###Taken from sejong_test.py

init_part = alt_gen_init_part(G, partition_number)
result_list, log_list = graph_simulated_annealing(G, init_part, iter_per_epoch, False)
compare_before_after_graph_anneal(G, init_part,result_list)

score_history_list = log_list[0]
probability_history_list = log_list[1]
min_score_list = log_list[2]


score_fig = plt.figure(1)
plt.plot(score_history_list)
plt.title(region_name +' Score Graph')
plt.savefig(region_name+'_score_history.png')
plt.close(score_fig)
prob_fig = plt.figure(2)
plt.plot(probability_history_list)
plt.title(region_name + ' Probability Graph')
plt.savefig(region_name+'_prob_history.png')
plt.close(prob_fig)

#print(score_history_list)
#print(probability_history_list)
#print('is planar?(new_Sejong_G): ',nx.is_planar(new_Sejong_G))
#print('is planar?(normalized_Sejong_G): ',nx.is_planar(normalized_Sejong_G))
print(min_score_list)

compare_before_after_graph_anneal(G, init_part,min_score_list[1])
sejong_test_file = open(region_name+'_test_log.txt','a')
sejong_test_file.write('====================\n')
sejong_test_file.writelines(str(datetime.datetime.now()) + str('\n'))
sejong_test_file.write('Initial Partition: \n')
sejong_test_file.writelines([str(x) for x in init_part])
sejong_test_file.writelines(['\nInitial Partition Score: ', str(score_history_list[0])])
sejong_test_file.write('\nFinal Anneal Partition: ')
sejong_test_file.writelines([str(x) for x in result_list])
sejong_test_file.writelines(['\nFinal Anneal Score: ', str(score_history_list[-1])])
sejong_test_file.write('\nMin Anneal Partition: ')
sejong_test_file.writelines([str(x) for x in min_score_list[1]])
sejong_test_file.writelines(['\nMin Anneal Score: ', str(min_score_list[0])])
sejong_test_file.write('\n===================\n')
sejong_test_file.close()

for i in G.nodes():
    if i in init_part[0]:
        G.nodes[i][Dict_Trait.color] = 0
    else:
        G.nodes[i][Dict_Trait.color] = 1

color_state_map = {0: 'blue', 1: 'red'}
nx.draw(G, node_color=[color_state_map[node[1][Dict_Trait.color]] for node in G.nodes(data=True)], with_labels=True)
plt.savefig(region_name+'_test_init_part_graph.png')
plt.close()


current_boundary_1 = [3011051500, 3011054500, 3011053000, 3011055100, 3011055200, 3011056000, 3011058500, 3011059000, 3011062000, 3011063000, 3011064000, 3011066500, 3011067000, 3011069500, 3011072500, 3011074000  ]
current_boundary_2 = [3014053500, 3014055000, 3014056000, 3014057500, 3014060500, 3014062000, 3014063000, 3014064000, 3014065500, 3014067000, 3014068000, 3014069000, 3014070000, 3014071000, 3014072000, 3014073000, 3014074000  ]
current_boundary_3 = [3017051000, 3017052000, 3017053000, 3017053500, 3017054000, 3017056000, 3017057000, 3017057500, 3017059000, 3017059600, 3017059700, 3017060000  ]
current_boundary_4 = [3017055000, 3017055500, 3017063000, 3017064000, 3017066000, 3017058100, 3017058200, 3017058600, 3017058700, 3017058800, 3017065000  ]
current_boundary_5 = [3020052000, 3020061000, 3020053000, 3020054000, 3020054600  ]
current_boundary_6 = [3020054700, 3020054800, 3020055000, 3020057000, 3020058000, 3020060000  ]
current_boundary_7 = [3023051000, 3023052000, 3023052500, 3023053300, 3023054300, 3023054600, 3023060000, 3023061000, 3023055000, 3023056000, 3023057000, 3023058000  ]



current_boundary = [current_boundary_1,current_boundary_2, current_boundary_3,current_boundary_4,current_boundary_5,current_boundary_6,current_boundary_7]
min_part =[
              [3017058200, 3017058700, 3017063000, 3017064000, 3017065000, 3020054000,
 3020055000, 3023052000, 3023060000],
              [3017058600 ,3017059600, 3017060000, 3020052000 ,3020053000 ,3020054600,
 3020054700, 3020054800, 3020061000],
              [3014069000 ,3014070000 ,3014073000 ,3017051000 ,3017052000 ,3017053000,
 3017054000, 3017055000, 3017057000, 3017057500, 3017058100, 3017058800],
              [3011053000 ,3011055100 ,3011074000, 3014060500, 3014074000, 3017053500,
 3017059000 ,3017059700],
              [3011051500 ,3011054500 ,3011058500 ,3011059000, 3011063000, 3011064000,
 3011066500, 3011067000, 3014053500, 3014057500, 3014062000, 3014063000,
 3014064000, 3023054300 ,3023054600],
          [3011055200 ,3011056000 ,3011072500, 3020057000 ,3020058000, 3020060000,
 3023052500 ,3023053300 ,3023055000 ,3023056000 ,3023057000, 3023058000,
 3023061000],
          [3011062000 ,3011069500, 3014055000, 3014056000, 3014065500, 3014067000,
 3014068000 ,3014071000 ,3014072000, 3017055500 ,3017056000, 3017066000,
 3023051000]]
compare_before_after_graph_anneal(G, current_boundary,min_part)

#min partition color
for i in G.nodes():
    if i in min_part[0]:
        G.nodes[i][Dict_Trait.color] = 0
    else:
        G.nodes[i][Dict_Trait.color] = 1
nx.draw(G, node_color=[color_state_map[node[1][Dict_Trait.color]] for node in G.nodes(data=True)], with_labels=True)
plt.savefig(region_name+'_test_min_part_graph.png')
plt.close()
