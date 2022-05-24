from main import *

Dict_format = dict(
    {'name': 'default', 'id': 0, 'pop': 0, 'total_votes': 0, 'party_1': 0, 'party_2': 0, 'color': 'white'})
Dict_example = dict(
    {Dict_Trait.name: 'default', Dict_Trait.id: 0, Dict_Trait.pop: 0, Dict_Trait.total_votes: 0, Dict_Trait.party_1: 0,
     Dict_Trait.party_2: 0, Dict_Trait.party_3: 0, Dict_Trait.color: 'white'})



#Sejong Demo:
#described in sejong.adjlist
#Consists of 22 nodes and 2 districts

new_temp_G = nx.Graph()
new_adj_list_path = 'sejong_auto.adjlist'
new_temp_G = nx.read_adjlist(new_adj_list_path)
new_temp_adj_list = nx_gen_object_to_list(nx.generate_adjlist(new_temp_G))
new_Sejong_G_edge_list = []
for x in range(len(new_temp_adj_list)):
    #print(type(line))
    list_ = new_temp_adj_list[x].split(' ')
    list_ = [int(i) for i in list_]
    ele_list = []
    for y in range(1,len(list_)):
        ele_list.append((list_[0], list_[y]))
    new_Sejong_G_edge_list.extend(ele_list)
new_Sejong_G = nx.Graph()
new_Sejong_G.add_edges_from(new_Sejong_G_edge_list)
#merge
new_Sejong_G = nx.contracted_nodes(new_Sejong_G,3611011400,3611011000) #도담동, 어진동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G,3611010100, 3611011800) #반곡동, 집현동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G,3611010100, 3611011700) #반곡동, 합강동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G,3611010800, 3611010700) #새롬동, 나성동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G,3611010600, 3611010500) #한솔동, 가람동
new_Sejong_G = nx.contracted_nodes(new_Sejong_G,3611011600, 3611011500) #해밀동, 산울동
#remove self edges formed by merging
'''
new_Sejong_G.remove_edge(3611011400,3611011400) #도담동
new_Sejong_G.remove_edge(3611010100,3611010100) #반곡동
new_Sejong_G.remove_edge(3611010800,3611010800) #새롬동
new_Sejong_G.remove_edge(3611010600,3611010600) #한솔동
new_Sejong_G.remove_edge(3611011600,3611011600) #해밀동
'''
new_Sejong_G.remove_edges_from(nx.selfloop_edges(new_Sejong_G))
nx.write_adjlist(new_Sejong_G, "merged_sejong_auto.adjlist")
nx.draw(new_Sejong_G)
plt.show()


#gen_init_part(new_Sejong_G,2) #also does not seem to work with gen_init_part


temp_G = nx.Graph()
adj_list_path = 'sejong.adjlist'
temp_G = nx.read_adjlist(adj_list_path)
temp_adj_list = nx_gen_object_to_list(nx.generate_adjlist(temp_G))
print(temp_adj_list)
print(temp_adj_list[0].split(' '))
Sejong_G_edge_list = []
for x in range(len(temp_adj_list)):
    #print(type(line))
    list_ = temp_adj_list[x].split(' ')
    list_ = [int(i) for i in list_]
    ele_list = []
    for y in range(1,len(list_)):
        ele_list.append((list_[0], list_[y]))
    Sejong_G_edge_list.extend(ele_list)

    #list_ = [int(i) for i in line.split(' ')]
    #list_.pop(0)
    #temp_adj_list.append(list_)
#print(temp_adj_list)
print(Sejong_G_edge_list)
Sejong_G = nx.Graph()
Sejong_G.add_edges_from(Sejong_G_edge_list)
print(Sejong_G.number_of_nodes())

'''
#depreciated
sejong_3611055000 =dict({Dict_Trait.name: '고운동', Dict_Trait.id: 3611055000, Dict_Trait.pop: 34104, Dict_Trait.total_votes: 15230, Dict_Trait.party_1: 8489, Dict_Trait.party_2: 6058, Dict_Trait.party_3: 452, Dict_Trait.color: 'white'})
sejong_3611034000 =dict({Dict_Trait.name: '금남면', Dict_Trait.id: 3611034000, Dict_Trait.pop: 8917, Dict_Trait.total_votes: 5422, Dict_Trait.party_1: 2131, Dict_Trait.party_2: 3050, Dict_Trait.party_3: 127, Dict_Trait.color: 'white'})
sejong_3611058000 =dict({Dict_Trait.name: '다정동', Dict_Trait.id: 3611058000, Dict_Trait.pop: 28226, Dict_Trait.total_votes: 14980, Dict_Trait.party_1: 8046, Dict_Trait.party_2: 6199, Dict_Trait.party_3: 503, Dict_Trait.color: 'white'})
sejong_3611057000 =dict({Dict_Trait.name: '대평동', Dict_Trait.id: 3611057000, Dict_Trait.pop: 11316, Dict_Trait.total_votes: 6768, Dict_Trait.party_1: 3497, Dict_Trait.party_2: 2972, Dict_Trait.party_3: 206, Dict_Trait.color: 'white'})
sejong_3611052000 =dict({Dict_Trait.name: '도담동', Dict_Trait.id: 3611052000, Dict_Trait.pop: 33520, Dict_Trait.total_votes: 16618, Dict_Trait.party_1: 8589, Dict_Trait.party_2: 7238, Dict_Trait.party_3: 535, Dict_Trait.color: 'white'})
sejong_3611055600 =dict({Dict_Trait.name: '반곡동', Dict_Trait.id: 3611055600, Dict_Trait.pop: 22210, Dict_Trait.total_votes: 10594, Dict_Trait.party_1: 5631, Dict_Trait.party_2: 4415, Dict_Trait.party_3: 363, Dict_Trait.color: 'white'})
sejong_3611056000 =dict({Dict_Trait.name: '보람동', Dict_Trait.id: 3611056000, Dict_Trait.pop: 18852, Dict_Trait.total_votes: 10415, Dict_Trait.party_1: 5632, Dict_Trait.party_2: 4295, Dict_Trait.party_3: 330, Dict_Trait.color: 'white'})
sejong_3611033000 =dict({Dict_Trait.name: '부강면', Dict_Trait.id: 3611033000, Dict_Trait.pop: 6090, Dict_Trait.total_votes: 3881, Dict_Trait.party_1: 1719, Dict_Trait.party_2: 1968, Dict_Trait.party_3: 92, Dict_Trait.color: 'white'})
sejong_3611051500 =dict({Dict_Trait.name: '새롬동', Dict_Trait.id: 3611051500, Dict_Trait.pop: 39069, Dict_Trait.total_votes: 18210, Dict_Trait.party_1: 9557, Dict_Trait.party_2: 7854, Dict_Trait.party_3: 545, Dict_Trait.color: 'white'})
sejong_3611055500 =dict({Dict_Trait.name: '소담동', Dict_Trait.id: 3611055500, Dict_Trait.pop: 21004, Dict_Trait.total_votes: 10787, Dict_Trait.party_1: 5926, Dict_Trait.party_2: 4392, Dict_Trait.party_3: 320, Dict_Trait.color: 'white'})
sejong_3611039000 =dict({Dict_Trait.name: '소정면', Dict_Trait.id: 3611039000, Dict_Trait.pop: 2229, Dict_Trait.total_votes: 1374, Dict_Trait.party_1: 496, Dict_Trait.party_2: 810, Dict_Trait.party_3: 37, Dict_Trait.color: 'white'})
sejong_3611053000 =dict({Dict_Trait.name: '아름동', Dict_Trait.id: 3611053000, Dict_Trait.pop: 23291, Dict_Trait.total_votes: 12542, Dict_Trait.party_1: 7361, Dict_Trait.party_2: 4594, Dict_Trait.party_3: 433, Dict_Trait.color: 'white'})
sejong_3611031000 =dict({Dict_Trait.name: '연기면', Dict_Trait.id: 3611031000, Dict_Trait.pop: 2780, Dict_Trait.total_votes: 2819, Dict_Trait.party_1: 1349, Dict_Trait.party_2: 1346, Dict_Trait.party_3: 63, Dict_Trait.color: 'white'})
sejong_3611032000 =dict({Dict_Trait.name: '연동면', Dict_Trait.id: 3611032000, Dict_Trait.pop: 3086, Dict_Trait.total_votes: 1993, Dict_Trait.party_1: 728, Dict_Trait.party_2: 1181, Dict_Trait.party_3: 34, Dict_Trait.color: 'white'})
sejong_3611036000 =dict({Dict_Trait.name: '연서면', Dict_Trait.id: 3611036000, Dict_Trait.pop: 7336, Dict_Trait.total_votes: 5581, Dict_Trait.party_1: 2620, Dict_Trait.party_2: 2737, Dict_Trait.party_3: 101, Dict_Trait.color: 'white'})
sejong_3611035000 =dict({Dict_Trait.name: '장군면', Dict_Trait.id: 3611035000, Dict_Trait.pop: 7057, Dict_Trait.total_votes: 3931, Dict_Trait.party_1: 1796, Dict_Trait.party_2: 1974, Dict_Trait.party_3: 73, Dict_Trait.color: 'white'})
sejong_3611038000 =dict({Dict_Trait.name: '전동면', Dict_Trait.id: 3611038000, Dict_Trait.pop: 3359, Dict_Trait.total_votes: 1981, Dict_Trait.party_1: 731, Dict_Trait.party_2: 1161, Dict_Trait.party_3: 46, Dict_Trait.color: 'white'})
sejong_3611037000 =dict({Dict_Trait.name: '전의면', Dict_Trait.id: 3611037000, Dict_Trait.pop: 5524, Dict_Trait.total_votes: 3452, Dict_Trait.party_1: 1368, Dict_Trait.party_2: 1909, Dict_Trait.party_3: 87, Dict_Trait.color: 'white'})
sejong_3611025000 =dict({Dict_Trait.name: '조치원읍', Dict_Trait.id: 3611025000, Dict_Trait.pop: 43191, Dict_Trait.total_votes: 20910, Dict_Trait.party_1: 9666, Dict_Trait.party_2: 10152, Dict_Trait.party_3: 576, Dict_Trait.color: 'white'})
sejong_3611054000 =dict({Dict_Trait.name: '종촌동', Dict_Trait.id: 3611054000, Dict_Trait.pop: 28948, Dict_Trait.total_votes: 15674, Dict_Trait.party_1: 8662, Dict_Trait.party_2: 6362, Dict_Trait.party_3: 445, Dict_Trait.color: 'white'})
sejong_3611051000 =dict({Dict_Trait.name: '한솔동', Dict_Trait.id: 3611051000, Dict_Trait.pop: 18546, Dict_Trait.total_votes: 10184, Dict_Trait.party_1: 5599, Dict_Trait.party_2: 4140, Dict_Trait.party_3: 311, Dict_Trait.color: 'white'})
sejong_3611052500 =dict({Dict_Trait.name: '해밀동', Dict_Trait.id: 3611052500, Dict_Trait.pop: 8641, Dict_Trait.total_votes: 4589, Dict_Trait.party_1: 2670, Dict_Trait.party_2: 1726, Dict_Trait.party_3: 140, Dict_Trait.color: 'white'})
'''


sejong_3611011200 =dict({Dict_Trait.name: '고운동', Dict_Trait.id: 3611011200, Dict_Trait.pop: 34104, Dict_Trait.total_votes: 15230, Dict_Trait.party_1: 8489, Dict_Trait.party_2: 6058, Dict_Trait.party_3: 452, Dict_Trait.color: 'white'})
sejong_3611034000 =dict({Dict_Trait.name: '금남면', Dict_Trait.id: 3611034000, Dict_Trait.pop: 8917, Dict_Trait.total_votes: 5422, Dict_Trait.party_1: 2131, Dict_Trait.party_2: 3050, Dict_Trait.party_3: 127, Dict_Trait.color: 'white'})
sejong_3611010900 =dict({Dict_Trait.name: '다정동', Dict_Trait.id: 3611010900, Dict_Trait.pop: 28226, Dict_Trait.total_votes: 14980, Dict_Trait.party_1: 8046, Dict_Trait.party_2: 6199, Dict_Trait.party_3: 503, Dict_Trait.color: 'white'})
sejong_3611010400 =dict({Dict_Trait.name: '대평동', Dict_Trait.id: 3611010400, Dict_Trait.pop: 11316, Dict_Trait.total_votes: 6768, Dict_Trait.party_1: 3497, Dict_Trait.party_2: 2972, Dict_Trait.party_3: 206, Dict_Trait.color: 'white'})
sejong_3611011400 =dict({Dict_Trait.name: '도담동', Dict_Trait.id: 3611011400, Dict_Trait.pop: 33520, Dict_Trait.total_votes: 16618, Dict_Trait.party_1: 8589, Dict_Trait.party_2: 7238, Dict_Trait.party_3: 535, Dict_Trait.color: 'white'})
sejong_3611010100 =dict({Dict_Trait.name: '반곡동', Dict_Trait.id: 3611010100, Dict_Trait.pop: 22210, Dict_Trait.total_votes: 10594, Dict_Trait.party_1: 5631, Dict_Trait.party_2: 4415, Dict_Trait.party_3: 363, Dict_Trait.color: 'white'})
sejong_3611010300 =dict({Dict_Trait.name: '보람동', Dict_Trait.id: 3611010300, Dict_Trait.pop: 18852, Dict_Trait.total_votes: 10415, Dict_Trait.party_1: 5632, Dict_Trait.party_2: 4295, Dict_Trait.party_3: 330, Dict_Trait.color: 'white'})
sejong_3611033000 =dict({Dict_Trait.name: '부강면', Dict_Trait.id: 3611033000, Dict_Trait.pop: 6090, Dict_Trait.total_votes: 3881, Dict_Trait.party_1: 1719, Dict_Trait.party_2: 1968, Dict_Trait.party_3: 92, Dict_Trait.color: 'white'})
sejong_3611010800 =dict({Dict_Trait.name: '새롬동', Dict_Trait.id: 3611010800, Dict_Trait.pop: 39069, Dict_Trait.total_votes: 18210, Dict_Trait.party_1: 9557, Dict_Trait.party_2: 7854, Dict_Trait.party_3: 545, Dict_Trait.color: 'white'})
sejong_3611010200 =dict({Dict_Trait.name: '소담동', Dict_Trait.id: 3611010200, Dict_Trait.pop: 21004, Dict_Trait.total_votes: 10787, Dict_Trait.party_1: 5926, Dict_Trait.party_2: 4392, Dict_Trait.party_3: 320, Dict_Trait.color: 'white'})
sejong_3611039000 =dict({Dict_Trait.name: '소정면', Dict_Trait.id: 3611039000, Dict_Trait.pop: 2229, Dict_Trait.total_votes: 1374, Dict_Trait.party_1: 496, Dict_Trait.party_2: 810, Dict_Trait.party_3: 37, Dict_Trait.color: 'white'})
sejong_3611011300 =dict({Dict_Trait.name: '아름동', Dict_Trait.id: 3611011300, Dict_Trait.pop: 23291, Dict_Trait.total_votes: 12542, Dict_Trait.party_1: 7361, Dict_Trait.party_2: 4594, Dict_Trait.party_3: 433, Dict_Trait.color: 'white'})
sejong_3611031000 =dict({Dict_Trait.name: '연기면', Dict_Trait.id: 3611031000, Dict_Trait.pop: 2780, Dict_Trait.total_votes: 2819, Dict_Trait.party_1: 1349, Dict_Trait.party_2: 1346, Dict_Trait.party_3: 63, Dict_Trait.color: 'white'})
sejong_3611032000 =dict({Dict_Trait.name: '연동면', Dict_Trait.id: 3611032000, Dict_Trait.pop: 3086, Dict_Trait.total_votes: 1993, Dict_Trait.party_1: 728, Dict_Trait.party_2: 1181, Dict_Trait.party_3: 34, Dict_Trait.color: 'white'})
sejong_3611036000 =dict({Dict_Trait.name: '연서면', Dict_Trait.id: 3611036000, Dict_Trait.pop: 7336, Dict_Trait.total_votes: 5581, Dict_Trait.party_1: 2620, Dict_Trait.party_2: 2737, Dict_Trait.party_3: 101, Dict_Trait.color: 'white'})
sejong_3611035000 =dict({Dict_Trait.name: '장군면', Dict_Trait.id: 3611035000, Dict_Trait.pop: 7057, Dict_Trait.total_votes: 3931, Dict_Trait.party_1: 1796, Dict_Trait.party_2: 1974, Dict_Trait.party_3: 73, Dict_Trait.color: 'white'})
sejong_3611038000 =dict({Dict_Trait.name: '전동면', Dict_Trait.id: 3611038000, Dict_Trait.pop: 3359, Dict_Trait.total_votes: 1981, Dict_Trait.party_1: 731, Dict_Trait.party_2: 1161, Dict_Trait.party_3: 46, Dict_Trait.color: 'white'})
sejong_3611037000 =dict({Dict_Trait.name: '전의면', Dict_Trait.id: 3611037000, Dict_Trait.pop: 5524, Dict_Trait.total_votes: 3452, Dict_Trait.party_1: 1368, Dict_Trait.party_2: 1909, Dict_Trait.party_3: 87, Dict_Trait.color: 'white'})
sejong_3611025000 =dict({Dict_Trait.name: '조치원읍', Dict_Trait.id: 3611025000, Dict_Trait.pop: 43191, Dict_Trait.total_votes: 20910, Dict_Trait.party_1: 9666, Dict_Trait.party_2: 10152, Dict_Trait.party_3: 576, Dict_Trait.color: 'white'})
sejong_3611011100 =dict({Dict_Trait.name: '종촌동', Dict_Trait.id: 3611011100, Dict_Trait.pop: 28948, Dict_Trait.total_votes: 15674, Dict_Trait.party_1: 8662, Dict_Trait.party_2: 6362, Dict_Trait.party_3: 445, Dict_Trait.color: 'white'})
sejong_3611010600 =dict({Dict_Trait.name: '한솔동', Dict_Trait.id: 3611010600, Dict_Trait.pop: 18546, Dict_Trait.total_votes: 10184, Dict_Trait.party_1: 5599, Dict_Trait.party_2: 4140, Dict_Trait.party_3: 311, Dict_Trait.color: 'white'})
sejong_3611011600 =dict({Dict_Trait.name: '해밀동', Dict_Trait.id: 3611011600, Dict_Trait.pop: 8641, Dict_Trait.total_votes: 4589, Dict_Trait.party_1: 2670, Dict_Trait.party_2: 1726, Dict_Trait.party_3: 140, Dict_Trait.color: 'white'})




'''
3611010100	3611031000 3611034000 3611010200 3611032000
3611010200	3611031000 3611010100 3611034000 3611010300
3611010300	3611031000 3611010200 3611034000 3611010400
3611010400	3611031000 3611010300 3611034000
3611010600	3611010800 3611031000 3611035000 3611010800
3611010800	3611035000 3611010900 3611010600 3611010600 3611011400 3611031000
3611010900	3611011200 3611011100 3611011400 3611010800 3611010800 3611035000
3611011100	3611011200 3611011300 3611011400 3611011400 3611010900
3611011200	3611031000 3611011600 3611011300 3611011100 3611010900 3611035000
3611011300	3611011200 3611011600 3611011400 3611011100
3611011400	3611011600 3611011600 3611031000 3611011100 3611011300 3611010800 3611010900
3611011600	3611031000 3611011400 3611011300 3611011200
3611025000	3611038000 3611036000 3611032000
3611031000	3611036000 3611032000 3611010100 3611010100 3611010100
3611032000	3611025000 3611036000 3611031000 3611010100 3611034000 3611033000
3611033000	3611032000 3611034000
3611034000	3611035000 3611031000 3611010400 3611010300 3611010200 3611010100 3611010100 3611032000 3611033000
3611035000	3611036000 3611031000 3611011200 3611010900 3611010800 3611010600 3611034000
3611036000	3611037000 3611038000 3611025000 3611032000 3611031000 3611035000
3611037000	3611038000 3611036000
3611038000	3611037000 3611036000 3611025000
3611039000	3611037000
'''


'''
sejong_key_list = [3611055000,
3611034000,
3611058000,
3611057000,
3611052000,
3611055600,
3611056000,
3611033000,
3611051500,
3611055500,
3611039000,
3611053000,
3611031000,
3611032000,
3611036000,
3611035000,
3611038000,
3611037000,
3611025000,
3611054000,
3611051000,
3611052500,
]
'''

sejong_key_list =[3611011200,
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


'''
sejong_value_list = [sejong_3611055000,
sejong_3611034000,
sejong_3611058000,
sejong_3611057000,
sejong_3611052000,
sejong_3611055600,
sejong_3611056000,
sejong_3611033000,
sejong_3611051500,
sejong_3611055500,
sejong_3611039000,
sejong_3611053000,
sejong_3611031000,
sejong_3611032000,
sejong_3611036000,
sejong_3611035000,
sejong_3611038000,
sejong_3611037000,
sejong_3611025000,
sejong_3611054000,
sejong_3611051000,
sejong_3611052500
]
'''

sejong_dict = {sejong_key_list[i]: sejong_value_list[i] for i in range(len(sejong_key_list))}
print(len(sejong_dict))
print((sejong_dict))
print(Sejong_G.nodes())
print('dict')
for item in sejong_dict:
    print(sejong_dict[item])

#node_dict = {key_list[i]: value_list[i] for i in range(len(key_list))}
nx.set_node_attributes(Sejong_G, sejong_dict)
#pos_Sejong_G = nx.spring_layout(Sejong_G)
nx.draw(Sejong_G, with_labels=True)
plt.show()
print('\n')
print(list(Sejong_G.nodes(data=Dict_Trait.name)))

print(Sejong_G.nodes())
Sejong_G_node_list = [3611010100, 3611031000, 3611034000, 3611010200, 3611032000, 3611010300, 3611010400, 3611010600, 3611010800, 3611011200, 3611011400, 3611011600, 3611036000, 3611035000, 3611033000, 3611025000, 3611010900, 3611011100, 3611011300, 3611038000, 3611037000, 3611039000]
Sejong_G_part1_list = [3611010100, 3611031000, 3611034000, 3611010200, 3611010300, 3611010400, 3611010600, 3611010800, 3611011200, 3611011400, 3611011600, 3611035000, 3611033000, 3611010900, 3611011100, 3611011300]
Sejong_G_part2_list = [3611039000,3611037000,3611038000, 3611025000, 3611036000, 3611032000]
print(type(Sejong_G))
print('connected?')
print(nx.is_connected(Sejong_G.subgraph(Sejong_G_part1_list)))
print(nx.is_connected(Sejong_G.subgraph(Sejong_G_part1_list)))
#print(return_adj_list_of_graph(Sejong_G))
#print(nx.number_of_edges(Sejong_G))
#Sejong_init_part = gen_init_part(Sejong_G,2)
#print_node_list(Sejong_init_part)
#Use manual init_part because gen_init_part for Sejong_G causes the function to crash (could be problem with graph itself))
init_part = [Sejong_G_part1_list,Sejong_G_part2_list]

l,foo = graph_simulated_annealing(Sejong_G, init_part,1)
print('Initial:')
print(print_graph_result(*(calculate_graph_result(Sejong_G,init_part, True))))
print('Final')
print(print_graph_result(*(calculate_graph_result(Sejong_G,l, True))))
print_node_list(l)
print_node_list(init_part)
current_boundary_Sejong_A = [3611010600,3611011400, 3611010800,3611010400,3611010200,3611033000, 3611034000,3611035000]
current_boundary_Sejong_B = [3611010100, 3611031000, 3611032000, 3611010300, 3611011200, 3611011600, 3611036000, 3611025000, 3611010900, 3611011100, 3611011300, 3611038000, 3611037000, 3611039000]
current_boundary = [current_boundary_Sejong_A,current_boundary_Sejong_B]
print('Current Configuration')
print(print_graph_result(*(calculate_graph_result(Sejong_G,current_boundary, True))))
print_node_list(current_boundary)
plt.plot(foo)
#plt.yscale('log')
plt.xlabel('epoch')
plt.ylabel('score')
plt.show()
p_layout = nx.planar_layout(Sejong_G)

nx.draw(Sejong_G,p_layout)
plt.show()