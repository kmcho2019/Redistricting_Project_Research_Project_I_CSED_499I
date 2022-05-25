from main import *

Dict_format = dict(
    {'name': 'default', 'id': 0, 'pop': 0, 'total_votes': 0, 'party_1': 0, 'party_2': 0, 'color': 'white'})
Dict_example = dict(
    {Dict_Trait.name: 'default', Dict_Trait.id: 0, Dict_Trait.pop: 0, Dict_Trait.total_votes: 0, Dict_Trait.party_1: 0,
     Dict_Trait.party_2: 0, Dict_Trait.party_3: 0, Dict_Trait.color: 'white'})



#Sejong Demo:
#described in sejong.adjlist
#Consists of 22 nodes and 2 districts


new_adj_list_path = 'sejong_auto.adjlist'

new_Sejong_G = nx.read_adjlist(new_adj_list_path, nodetype=int)


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

for line in nx.generate_adjlist(new_Sejong_G):
    print(line)
print(list(nx.selfloop_edges(new_Sejong_G)))
new_Sejong_G.remove_edges_from(nx.selfloop_edges(new_Sejong_G))
nx.write_adjlist(new_Sejong_G, "merged_sejong_auto.adjlist")
nx.draw(new_Sejong_G)
plt.show()

p_layout = nx.planar_layout(new_Sejong_G)

nx.draw(new_Sejong_G,p_layout)
plt.show()

for line in nx.generate_adjlist(new_Sejong_G):
    print(line)

print([n for n in new_Sejong_G.neighbors(3611039000)])


normalization_list = []
for node_num in new_Sejong_G.nodes():
    l = [node_num]
    x = [n for n in new_Sejong_G.neighbors(node_num)]
    #print(l)
    #print(x)
    normalization_list.append([*l, *x])
    #print([*l, *x])

#print(normalization_list)

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

#gen_init_part(normalized_Sejong_G, 2)


#gen_init_part(new_Sejong_G,2) #also does not seem to work with gen_init_part


t = nx.is_isomorphic(new_Sejong_G,normalized_Sejong_G)
print(t)
#the fact that new_Sejong_G and normalized_Sejong_G is isometric shows that merging operation was done correctly

#normalization was conceived due to thoughts that incorrect merging operation led to malfunction of gen_init_part
#however was able to determine thanks to 'sejong_test.py' that the error was due to flaw in gen_init_part implementation

init_list = alt_gen_init_part(normalized_Sejong_G,2)
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