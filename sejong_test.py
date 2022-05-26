from main import *

Dict_format = dict(
    {'name': 'default', 'id': 0, 'pop': 0, 'total_votes': 0, 'party_1': 0, 'party_2': 0, 'color': 'white'})
Dict_example = dict(
    {Dict_Trait.name: 'default', Dict_Trait.id: 0, Dict_Trait.pop: 0, Dict_Trait.total_votes: 0, Dict_Trait.party_1: 0,
     Dict_Trait.party_2: 0, Dict_Trait.party_3: 0, Dict_Trait.color: 'white'})

# Sejong Demo:
# described in sejong.adjlist
# Consists of 22 nodes and 2 districts


new_adj_list_path = 'sejong_auto.adjlist'

new_Sejong_G = nx.read_adjlist(new_adj_list_path, nodetype=int)

# merge
new_Sejong_G = nx.contracted_nodes(new_Sejong_G, 3611011400, 3611011000)  # 도담동, 어진동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G, 3611010100, 3611011800)  # 반곡동, 집현동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G, 3611010100, 3611011700)  # 반곡동, 합강동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G, 3611010800, 3611010700)  # 새롬동, 나성동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G, 3611010600, 3611010500)  # 한솔동, 가람동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G, 3611011600, 3611011500)  # 해밀동, 산울동
# remove self edges formed by merging
'''
new_Sejong_G.remove_edge(3611011400,3611011400) #도담동
new_Sejong_G.remove_edge(3611010100,3611010100) #반곡동
new_Sejong_G.remove_edge(3611010800,3611010800) #새롬동
new_Sejong_G.remove_edge(3611010600,3611010600) #한솔동
new_Sejong_G.remove_edge(3611011600,3611011600) #해밀동
'''

for line in nx.generate_adjlist(new_Sejong_G):
    print(line)
print(list(nx.selfloop_edges(new_Sejong_G)))
new_Sejong_G.remove_edges_from(nx.selfloop_edges(new_Sejong_G))
nx.write_adjlist(new_Sejong_G, "merged_sejong_auto.adjlist")
nx.draw(new_Sejong_G)
plt.show()

p_layout = nx.planar_layout(new_Sejong_G)

nx.draw(new_Sejong_G, p_layout)
plt.show()

for line in nx.generate_adjlist(new_Sejong_G):
    print(line)

print([n for n in new_Sejong_G.neighbors(3611039000)])

normalization_list = []
for node_num in new_Sejong_G.nodes():
    l = [node_num]
    x = [n for n in new_Sejong_G.neighbors(node_num)]
    # print(l)
    # print(x)
    normalization_list.append([*l, *x])
    # print([*l, *x])

# print(normalization_list)

file1 = open('normalized_merged_sejong_auto.adjlist', 'w')
normalization_input_string = []
for list_ele in normalization_list:
    s = ''
    for i in range(len(list_ele)):
        if i != len(list_ele) - 1:
            s = s + str(list_ele[i]) + str(' ')
        else:
            s = s + str(list_ele[i]) + str('\n')
            normalization_input_string.append(s)

print(normalization_input_string)
file1.writelines(normalization_input_string)
file1.close()

normalized_Sejong_G = nx.Graph()
normalized_Sejong_G = nx.read_adjlist('normalized_merged_sejong_auto.adjlist', nodetype=int)
print(list(normalized_Sejong_G.nodes()))

for line in nx.generate_adjlist(normalized_Sejong_G):
    print(line)

print(list(normalized_Sejong_G.nodes()))

# gen_init_part(normalized_Sejong_G, 2)


# gen_init_part(new_Sejong_G,2) #also does not seem to work with gen_init_part


t = nx.is_isomorphic(new_Sejong_G, normalized_Sejong_G)
print(t)
# the fact that new_Sejong_G and normalized_Sejong_G is isometric shows that merging operation was done correctly

# normalization was conceived due to thoughts that incorrect merging operation led to malfunction of gen_init_part
# however was able to determine thanks to 'sejong_test.py' that the error was due to flaw in gen_init_part implementation

init_list = alt_gen_init_part(normalized_Sejong_G, 2)
subpart0 = normalized_Sejong_G.subgraph(init_list[0])
subpart1 = normalized_Sejong_G.subgraph(init_list[1])
subpart0_connected_state = nx.is_connected(subpart0)
subpart1_connected_state = nx.is_connected(subpart1)
print(init_list)
print(nx.is_connected(subpart0))
print(nx.is_connected(subpart1))
print(init_list[0])
print(init_list[1])
l = init_list[1]
l.sort()
print(l)

# Run District Formation process with new_Sejong_G (formed using automatic QGIS script)
sejong_3611011200 = dict(
    {Dict_Trait.name: '고운동', Dict_Trait.id: 3611011200, Dict_Trait.pop: 34104, Dict_Trait.total_votes: 15230,
     Dict_Trait.party_1: 8489, Dict_Trait.party_2: 6058, Dict_Trait.party_3: 452, Dict_Trait.color: 'white'})
sejong_3611034000 = dict(
    {Dict_Trait.name: '금남면', Dict_Trait.id: 3611034000, Dict_Trait.pop: 8917, Dict_Trait.total_votes: 5422,
     Dict_Trait.party_1: 2131, Dict_Trait.party_2: 3050, Dict_Trait.party_3: 127, Dict_Trait.color: 'white'})
sejong_3611010900 = dict(
    {Dict_Trait.name: '다정동', Dict_Trait.id: 3611010900, Dict_Trait.pop: 28226, Dict_Trait.total_votes: 14980,
     Dict_Trait.party_1: 8046, Dict_Trait.party_2: 6199, Dict_Trait.party_3: 503, Dict_Trait.color: 'white'})
sejong_3611010400 = dict(
    {Dict_Trait.name: '대평동', Dict_Trait.id: 3611010400, Dict_Trait.pop: 11316, Dict_Trait.total_votes: 6768,
     Dict_Trait.party_1: 3497, Dict_Trait.party_2: 2972, Dict_Trait.party_3: 206, Dict_Trait.color: 'white'})
sejong_3611011400 = dict(
    {Dict_Trait.name: '도담동', Dict_Trait.id: 3611011400, Dict_Trait.pop: 33520, Dict_Trait.total_votes: 16618,
     Dict_Trait.party_1: 8589, Dict_Trait.party_2: 7238, Dict_Trait.party_3: 535, Dict_Trait.color: 'white'})
sejong_3611010100 = dict(
    {Dict_Trait.name: '반곡동', Dict_Trait.id: 3611010100, Dict_Trait.pop: 22210, Dict_Trait.total_votes: 10594,
     Dict_Trait.party_1: 5631, Dict_Trait.party_2: 4415, Dict_Trait.party_3: 363, Dict_Trait.color: 'white'})
sejong_3611010300 = dict(
    {Dict_Trait.name: '보람동', Dict_Trait.id: 3611010300, Dict_Trait.pop: 18852, Dict_Trait.total_votes: 10415,
     Dict_Trait.party_1: 5632, Dict_Trait.party_2: 4295, Dict_Trait.party_3: 330, Dict_Trait.color: 'white'})
sejong_3611033000 = dict(
    {Dict_Trait.name: '부강면', Dict_Trait.id: 3611033000, Dict_Trait.pop: 6090, Dict_Trait.total_votes: 3881,
     Dict_Trait.party_1: 1719, Dict_Trait.party_2: 1968, Dict_Trait.party_3: 92, Dict_Trait.color: 'white'})
sejong_3611010800 = dict(
    {Dict_Trait.name: '새롬동', Dict_Trait.id: 3611010800, Dict_Trait.pop: 39069, Dict_Trait.total_votes: 18210,
     Dict_Trait.party_1: 9557, Dict_Trait.party_2: 7854, Dict_Trait.party_3: 545, Dict_Trait.color: 'white'})
sejong_3611010200 = dict(
    {Dict_Trait.name: '소담동', Dict_Trait.id: 3611010200, Dict_Trait.pop: 21004, Dict_Trait.total_votes: 10787,
     Dict_Trait.party_1: 5926, Dict_Trait.party_2: 4392, Dict_Trait.party_3: 320, Dict_Trait.color: 'white'})
sejong_3611039000 = dict(
    {Dict_Trait.name: '소정면', Dict_Trait.id: 3611039000, Dict_Trait.pop: 2229, Dict_Trait.total_votes: 1374,
     Dict_Trait.party_1: 496, Dict_Trait.party_2: 810, Dict_Trait.party_3: 37, Dict_Trait.color: 'white'})
sejong_3611011300 = dict(
    {Dict_Trait.name: '아름동', Dict_Trait.id: 3611011300, Dict_Trait.pop: 23291, Dict_Trait.total_votes: 12542,
     Dict_Trait.party_1: 7361, Dict_Trait.party_2: 4594, Dict_Trait.party_3: 433, Dict_Trait.color: 'white'})
sejong_3611031000 = dict(
    {Dict_Trait.name: '연기면', Dict_Trait.id: 3611031000, Dict_Trait.pop: 2780, Dict_Trait.total_votes: 2819,
     Dict_Trait.party_1: 1349, Dict_Trait.party_2: 1346, Dict_Trait.party_3: 63, Dict_Trait.color: 'white'})
sejong_3611032000 = dict(
    {Dict_Trait.name: '연동면', Dict_Trait.id: 3611032000, Dict_Trait.pop: 3086, Dict_Trait.total_votes: 1993,
     Dict_Trait.party_1: 728, Dict_Trait.party_2: 1181, Dict_Trait.party_3: 34, Dict_Trait.color: 'white'})
sejong_3611036000 = dict(
    {Dict_Trait.name: '연서면', Dict_Trait.id: 3611036000, Dict_Trait.pop: 7336, Dict_Trait.total_votes: 5581,
     Dict_Trait.party_1: 2620, Dict_Trait.party_2: 2737, Dict_Trait.party_3: 101, Dict_Trait.color: 'white'})
sejong_3611035000 = dict(
    {Dict_Trait.name: '장군면', Dict_Trait.id: 3611035000, Dict_Trait.pop: 7057, Dict_Trait.total_votes: 3931,
     Dict_Trait.party_1: 1796, Dict_Trait.party_2: 1974, Dict_Trait.party_3: 73, Dict_Trait.color: 'white'})
sejong_3611038000 = dict(
    {Dict_Trait.name: '전동면', Dict_Trait.id: 3611038000, Dict_Trait.pop: 3359, Dict_Trait.total_votes: 1981,
     Dict_Trait.party_1: 731, Dict_Trait.party_2: 1161, Dict_Trait.party_3: 46, Dict_Trait.color: 'white'})
sejong_3611037000 = dict(
    {Dict_Trait.name: '전의면', Dict_Trait.id: 3611037000, Dict_Trait.pop: 5524, Dict_Trait.total_votes: 3452,
     Dict_Trait.party_1: 1368, Dict_Trait.party_2: 1909, Dict_Trait.party_3: 87, Dict_Trait.color: 'white'})
sejong_3611025000 = dict(
    {Dict_Trait.name: '조치원읍', Dict_Trait.id: 3611025000, Dict_Trait.pop: 43191, Dict_Trait.total_votes: 20910,
     Dict_Trait.party_1: 9666, Dict_Trait.party_2: 10152, Dict_Trait.party_3: 576, Dict_Trait.color: 'white'})
sejong_3611011100 = dict(
    {Dict_Trait.name: '종촌동', Dict_Trait.id: 3611011100, Dict_Trait.pop: 28948, Dict_Trait.total_votes: 15674,
     Dict_Trait.party_1: 8662, Dict_Trait.party_2: 6362, Dict_Trait.party_3: 445, Dict_Trait.color: 'white'})
sejong_3611010600 = dict(
    {Dict_Trait.name: '한솔동', Dict_Trait.id: 3611010600, Dict_Trait.pop: 18546, Dict_Trait.total_votes: 10184,
     Dict_Trait.party_1: 5599, Dict_Trait.party_2: 4140, Dict_Trait.party_3: 311, Dict_Trait.color: 'white'})
sejong_3611011600 = dict(
    {Dict_Trait.name: '해밀동', Dict_Trait.id: 3611011600, Dict_Trait.pop: 8641, Dict_Trait.total_votes: 4589,
     Dict_Trait.party_1: 2670, Dict_Trait.party_2: 1726, Dict_Trait.party_3: 140, Dict_Trait.color: 'white'})

sejong_key_list = [3611011200,
                   3611034000,
                   3611010900,
                   3611010400,
                   3611011400,
                   3611010100,
                   3611010300,
                   3611033000,
                   3611010800,
                   3611010200,
                   3611039000,
                   3611011300,
                   3611031000,
                   3611032000,
                   3611036000,
                   3611035000,
                   3611038000,
                   3611037000,
                   3611025000,
                   3611011100,
                   3611010600,
                   3611011600
                   ]

sejong_value_list = [sejong_3611011200,
                     sejong_3611034000,
                     sejong_3611010900,
                     sejong_3611010400,
                     sejong_3611011400,
                     sejong_3611010100,
                     sejong_3611010300,
                     sejong_3611033000,
                     sejong_3611010800,
                     sejong_3611010200,
                     sejong_3611039000,
                     sejong_3611011300,
                     sejong_3611031000,
                     sejong_3611032000,
                     sejong_3611036000,
                     sejong_3611035000,
                     sejong_3611038000,
                     sejong_3611037000,
                     sejong_3611025000,
                     sejong_3611011100,
                     sejong_3611010600,
                     sejong_3611011600,
                     ]

sejong_dict = {sejong_key_list[i]: sejong_value_list[i] for i in range(len(sejong_key_list))}
nx.set_node_attributes(new_Sejong_G, sejong_dict)
init_part = alt_gen_init_part(new_Sejong_G, 2)
result_list, score_history_list = graph_simulated_annealing(new_Sejong_G, init_part, 100, True)
