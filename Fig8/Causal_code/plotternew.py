import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
import initialise.initialise as initialise
import initialise.parser as parser
import copy
import sys
#print("modules")
# import os

def plot_bar(filename, id_to_node, params):
    filename_index = 0
    for i in range(len(params['input_filenames'])):
        if "{}_".format(params['input_filenames'][i]) in filename:
            filename_index = i
            break
    per=100
    ac=2
    # probjsd_file1 = open("{}_jsd_1.txt".format(filename), 'w')
    length=len(id_to_node) - params['constant_node_count'][filename_index]
    # filematrix=[probjsd_file1]*(2**length)
    # for k in range(1,2**length    +1):
    #     filematrix[k-1]=open("{}_jsd_{}.txt".format(filename,k), 'w')
    # probjsd_file1.close()
    # prob_matrix = np.zeros((params['num_runs'], 2 ** (len(id_to_node) - params['constant_node_count'][filename_index])))
    prob_matrix = [{}] * params['num_runs']
    sprob_matrix = [{}] * params['num_runs']
    gene_id_fin = [id_to_node[i] for i in range(params['constant_node_count'][filename_index], len(id_to_node))]
    string_setbin = "{0:0" + str(len(id_to_node) - params['constant_node_count'][filename_index]) + "b}"
    # set_bin_fin = [string_setbin.format(i) for i in range(2 ** (len(id_to_node) - params['constant_node_count'][filename_index]))]
    #print(set_bin_fin)
    for cur_run in range(params['num_runs']):
        #print(cur_run)
        data = pd.read_csv("{}/{}_ss_run{}.txt".format(params['output_folder_name'], filename, cur_run+1), sep = " ", index_col = False)
        #print(data)
        gene_id = list(data.columns)[1:]
        data = data.to_numpy()[:,1:]
        for i in range(params['constant_node_count'][filename_index]):
            gene_id.remove(id_to_node[i])
        # print(data, params['constant_node_count'][filename_index])
        data = data[:, params['constant_node_count'][filename_index]:]
        #print(prob_matrix[cur_run])
        #print("_________________00__________________________________\n")

        # print(data, gene_id)
        # exit(0)
        # set_bin = {}
        # for t in range(0,2**length):
        #     k=t
        #     tempstr=''
        #     q1=0
        #     while(q1<length      ):
        #         if(k%2==0):
        #             tempstr+='1'
        #         else:
        #             tempstr+='0'
        #         k=k//2
        #         q1+=1
        #     set_bin.add(tempstr)
        # set_bin = sorted(set_bin)
        #print(set_bin)
        # for i in data:
        #    tempstr = ""
        #    for j in i:
        #        tempstr += '0' if j < 0 else '1'
        #    set_bin.add(tempstr)
        # set_bin = sorted(set_bin)
        # count = np.zeros(len(set_bin))
        for i in data:
            tempstr = ""
            for j in i:
                tempstr += '0' if j < 0 else '1'
            nodeval = int(tempstr, 2)
            # set_bin[nodeval] = nodeval
            try:
                prob_matrix[cur_run][nodeval] += 1
            except:
                prob_matrix[cur_run][nodeval] = 0
            # for j in range(len(set_bin)):
            #     if tempstr == set_bin[j]:
            #         count[j] += 1
            #         prob_matrix[cur_run][int(tempstr,2)] += 1
        # count /= params['num_simulations']
        # print(count)
        # prob_matrix.append(count)
        #print(count)
        #print(prob_matrix[0])
        #print("__________________test_________________________________\n")
        for i in prob_matrix[cur_run].keys():
            prob_matrix[cur_run][i] /= params['num_simulations']

        prob_file = open("{}/{}_ssprob_run{}.txt".format(params['output_folder_name'], filename, cur_run+1), 'w')
        for i in prob_matrix[cur_run].keys():
            prob_file.write("{} {}\n".format(string_setbin.format(i), prob_matrix[cur_run][i]))
        sprob_matrix[cur_run]=dict(prob_matrix[cur_run])
        prob_matrix[cur_run].clear()

        #print(sprob_matrix[cur_run])
        #print("________________________________________________\n")
        #print(sprob_matrix[ max(cur_run - 1, 0)])
        #print("________________________________________________\n")
            # if(i!=len(set_bin)-1):
            #     filematrix[ cur_run//(ac*per)  ].write("{} ".format(count[i]))
            # else:
            #     filematrix[ cur_run//(ac*per)  ].write("{}".format(count[i]))
        # if(cur_run+1 %(ac*per) !=0):
        #     filematrix[ cur_run//(ac*per)  ].write("\n")
        prob_file.close()
    #for i in range(params['num_runs']):
    #    print(i)
    #    print(sprob_matrix[i])
    #    print("________________________________________________\n")
    prob_matrix = copy.deepcopy(sprob_matrix)
    # for k in range(0,2**length):
    #     filematrix[k].close()
    # error = np.zeros(len(set_bin_fin))
    # final = np.zeros(len(set_bin_fin))
    error = {}
    final = {}
    finalin=[i for i in range(len(prob_matrix[0].keys()))]
    # errortop = [0]*int(len(set_bin_fin))
    # errorbot = [0]*int(len(set_bin_fin))
    yterr = {}
    # prob_matrix = np.matrix(prob_matrix)/params['num_simulations']

    keys_arr = {}
    keys_list = []
    probmatrix_final = []
    counter_index = 0

    for i in range(params['num_runs']):
        for j in prob_matrix[i].keys():
            if j not in keys_arr.keys():
                keys_list.append(j)
                keys_arr[j] = counter_index
                counter_index += 1

    #for i in range(params['num_runs']):
    #    print(prob_matrix[i])
    #    print("________________________________________________\n")
    for i in range(params['num_runs']):
        temparr = [0] * len(keys_arr.keys())
        for j in prob_matrix[i].keys():
            if j in keys_arr.keys():
                temparr[keys_arr[j]] = prob_matrix[i][j]
        ##print(temparr)
        ##print("________________________________________________\n")
        probmatrix_final.append(temparr)

    prob_matrix = np.matrix(probmatrix_final)
    #print(prob_matrix)
    error = [0 for i in range(len(keys_arr.keys()))]
    final = [0 for i in range(len(keys_arr.keys()))]
    final_index=[i for i in range(len(keys_arr.keys()))]
    yterr = [[0] * len(final), [0] * len(final)]
    # print(prob_matrix)
    # keyvals = list(prob_matrix[0].keys())
    for i in range(len(keys_arr.keys())):
        # print(prob_matrix)
        curvec = []

        error[i] = np.std(prob_matrix[:,i])
        final[i] = np.mean(prob_matrix[:,i])
        #print(error[i])
        dev1=0
        dev2=0
        cnt1=0
        cnt2=0
        arr1=prob_matrix[:,i]
        for v in range(params['num_runs']):
            if(arr1[v]>=final[i]):
                dev1+=(arr1[v]-final[i])**2
                cnt1+=1
            else:
                dev2+=(arr1[v]-final[i])**2
                cnt2+=1
        if(cnt1!=0):
            yterr[1][i]=math.sqrt(dev1/cnt1)
        if(cnt2!=0):
            yterr[0][i]=math.sqrt(dev2/cnt2)
        #print(dev1,dev2,cnt1,cnt2)
        #print(prob_matrix[:,i],error[i],final[i])
    # print(final, error, set_bin)
    #print(cnt1,cnt2)
    #print(final)
    x_label = "States: "
    for i in gene_id:
        x_label += i + " "
    remove_index = []
    for i in range(len(final)):
        if final[i] == 0:
            remove_index.append(i)
    num_cycles = 0

    for temp in remove_index:
        i = temp - num_cycles
        final.remove(final[i])
        #final_index.remove(final_index[i])
        error.remove(error[i])
        keys_list.remove(keys_list[i])
        #errorbot.remove(errorbot[i])
        #errortop.remove(errortop[i])
        yterr[0].remove(yterr[0][i])
        yterr[1].remove(yterr[1][i])
        num_cycles += 1

    prob_file = open("{}/{}_ssprob_all.txt".format(params['output_folder_name'], filename), 'w')
    prob_file.write("Node_Config Probability Error\n")
    for i in range(len(final)):
        prob_file.write("{} {:.6f} {:.6f}\n".format(string_setbin.format(keys_list[i]), final[i], error[i]))
    prob_file.close()

    notfinal_index = []
    notfinal= []
    notset_bin_fin= []
    notyterr0= []
    notyterr1= []

    for i in range(len(final)):
        if final[i] < 0.01:
            notfinal_index.append(i)
            notfinal.append(final[i])
            notset_bin_fin.append((keys_list[i]))
            notyterr0.append( yterr[0][i])
            notyterr1.append( yterr[1][i])

    for i in range(len(notfinal_index)):
        final.remove(notfinal[i])
        keys_list.remove(notset_bin_fin[i])
        yterr[0].remove(notyterr0[i])
        yterr[1].remove(notyterr1[i])
       # final_index.remove( notfinal_index[i])


    argarr = np.argsort(final)[::-1]
    checkarr=[0]*len(argarr)
    listarr=[0]*len(argarr)


    set_bin_fin = [string_setbin.format(keys_list[i]) for i in argarr]

    final = [final[i] for i in argarr]

    yterr[0] = [yterr[0][i] for i in argarr]
    yterr[1] = [yterr[1][i] for i in argarr]



    rcParams.update({'figure.autolayout':True}) #NOTE!!!!!!!!! properly resizes things :D
    plt.figure(figsize = (20,10))
    plt.subplots_adjust(0.1, 0.5, 0.9, 0.9)
    plt.title("{}_steady_states".format(filename))
    plt.xlabel(x_label)
    #print(x_label)
    plt.xticks(rotation = 'vertical')

    plt.bar(set_bin_fin,final,yerr=yterr,capsize = 5)
    # try:
    #     os.chdir('graphs')
    # except:
    #     print("dir graphs exists")
    plt.savefig("{}/{}/{}_ss_barplot.png".format(params['output_folder_name'], 'graphs',filename))


in_file = sys.argv[1]
max_initlines = 14
begin=1
process_count=1
params = initialise.initialise(in_file, max_initlines)
params['file_reqs'] = initialise.set_file_reqs(params)
for i in params['file_reqs']:
    for j in params['input_filenames']:
                random_seed = int(begin) + process_count
                weighted_tick = 1 if "_weigh" in i else 0
                async_tick = 1 if "_async" in i else 0
                link_matrix, id_to_node = parser.parse_topo(params,j,weighted_tick, random_seed)
                #print(params)
                plot_bar(j+i,id_to_node,params)

                #if(cur_run%100==0):
                #    print(link_matrix)
                # link_matrix_list.append(link_matrix)
                # id_to_node_list.append(id_to_node)
                # print(link_matrix)
                # print(id_to_node)
                # exit(0)
