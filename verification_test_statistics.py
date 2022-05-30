##Repeat the process of simulated annealing for graph in verification_test.py
# This is meant to generate statistics on the effectiveness of annealing algorithm compared to possible permutation
import numpy as np

from main import *
from scipy import stats
from verification_test import *
import statistics
columns = ['score']
r_df = pd.read_csv('Contiguous_Graph_Score.csv', usecols=columns)
print(r_df)
contig_score = r_df.values
contig_score = [x[0] for x in contig_score]
#df.plot.hist(grid=True, bins ='auto',rwidth= 0.9)
plt.hist(contig_score, bins= 100)
plt.title('Score of All Contiguous Graphs')
plt.xlabel('Score')
plt.ylabel('Counts')
plt.xticks([x/10. for x in range(11)])
plt.grid(axis ='y', alpha =0.5)
plt.savefig('Contiguous_Graph_Histogram.png')
plt.close()

plt.hist(contig_score, bins= 2000)
plt.title('0.0-0.005 Score Portion of Contiguous Graphs')
plt.xlabel('Score')
plt.ylabel('Counts')
#plt.xticks([x/10. for x in range(11)])
#a = plt.axes([x/50. for x in range(11)])
plt.grid(axis ='y', alpha =0.5)
plt.xticks([x/1000. for x in range(6)])
plt.xlim(-0.0005,0.0055)
plt.margins(x=-0.45, y =0.0)
#plt.setp(a, xticks=[x/50. for x in range(11)])
plt.savefig('Partial_Contiguous_Graph_Histogram.png')
plt.close()

simulated_score = []
for x in range(1000):
    init_part = alt_gen_init_part(G, 2)
    result_list, log_list = graph_simulated_annealing(G, init_part, 10, False)
    trial_min_score = log_list[2][0]
    simulated_score.append(trial_min_score)

input_dict = {'score': simulated_score}
df = pd.DataFrame(input_dict)
df.to_csv('Verification_Simulation_result.csv')

simulation_average = sum(simulated_score)/len(simulated_score)#int(np.mean(simulated_score))
simulation_5_percentile = np.percentile(simulated_score, 5)
simulation_95_percentile = np.percentile(simulated_score, 95)
simulation_max = max(simulated_score)
simulation_min = min(simulated_score)
a = stats.percentileofscore(r_df['score'], simulation_average)
b = stats.percentileofscore(r_df['score'], simulation_5_percentile)
c = stats.percentileofscore(r_df['score'], simulation_95_percentile)
d = stats.percentileofscore(r_df['score'], simulation_max)
e = stats.percentileofscore(r_df['score'], simulation_min)
f = open('verifcation_simulation_percentile_result.txt', 'w')
f.write('average, 5th percentile, 95th percentile, max, min\n')
f.writelines([str(simulation_average),', ', str(simulation_5_percentile),', ',str(simulation_95_percentile),', ',str(simulation_max),', ', str(simulation_min), '\n'])
f.writelines([str(a),'%, ',str(b),'%, ',str(c),'%, ',str(d),'%, ',str(e),'%\n'])
f.close()