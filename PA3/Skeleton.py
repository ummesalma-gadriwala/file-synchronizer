import itertools
from collections import defaultdict
import sys

def diameter (nodes, G):
    #YOUR CODE
"""
Input: 
-    List “nodes” containing node IDs 
-    Dictionary “G” with (keys = node IDs) and 
    (values = list of neighbor IDs for each node)
Returns: 
-    a Boolean value indicates if the graph G is a spanning tree 
    (covering and loop-free) or not 
"""
    return Diameter

def check_spanning_tree(nodes, G):
    #YOUR CODE
"""
Input: 
-    List “nodes” containing node IDs 
-    Dictionary “G” with (keys = node IDs) and (values = list of neighbor IDs for each node)
Returns: 
-    The diameter of graph G as an integer number
"""
    return isSpanningTree

def get_choices (L, excludes):
    choices = []
    for i in range(1, 2**len(L)):
        l = []
        good = True
        for j in range(len(L) + 1):
            if (i >= (2 ** j) and i % (2 ** (j + 1)) != 0):
                if (L[j] > excludes):
                    l.append (L[j])
                else:
                    good = False
                    break
        if (good):
            choices.append(l)
    return choices

def print_tree (Tree):
    print("*** SPANNING TREE ***")
    for sw,ports in Tree.iteritems():
      print((" %i : " % sw) + " ".join([str(l[0]) for l in
                                           sorted(list(ports))]))
    print("*********************")


switches = set([1, 2, 3, 4, 5, 6, 7])

adj = defaultdict(lambda:defaultdict(lambda:[]))

adj[1][2] = 2
adj[2][1] = 3
adj[1][7] = 3
adj[7][1] = 6
adj[2][3] = 2
adj[3][2] = 3
adj[2][7] = 4
adj[7][2] = 5
adj[3][4] = 2
adj[4][3] = 3
adj[3][7] = 4
adj[7][3] = 4
adj[4][5] = 2
adj[5][4] = 3
adj[4][7] = 4
adj[7][4] = 3
adj[5][7] = 4
adj[7][5] = 2
adj[6][7] = 3
adj[7][6] = 1

tree = defaultdict(set)
if (len(sys.argv) > 1 and str(sys.argv[1]) == "--mdst"):

    Choices = {}
    selectedChoice = {}
    ls = sorted(list(switches))
    
    for i in ls:
        Choices[i] = get_choices(list(adj[i]), i)
        selectedChoice[i] = 0

    finish = False
    md = 100
    while (not finish):
        nextTree = defaultdict(set)
        for i in ls:
            selectedChoice[i] = selectedChoice[i] + 1
            if (selectedChoice[i] >= len(Choices[i])):
                selectedChoice[i] = 0
                if (i == ls[len(ls) - 1]):
                    finish = True
            else:
                break
        
        graph = {}        
        for j in switches:
            graph[j] = [] 
            
        for j in switches:
            if(len(Choices[j]) > 0):
                for k in Choices[j][selectedChoice[j]]:
                    if not ((k,adj[j][k]) in nextTree[j]):
                        graph[j].append(k) 
                        graph[k].append(j)
                        nextTree[j].add((k,adj[j][k])) 
                        nextTree[k].add((j,adj[k][j])) 
        if (check_spanning_tree(ls, graph)):
            d = diameter(ls, graph)
            if (d < md):
                md = d
                tree = nextTree

else:
    done = set()
    more = set(switches)
    q=[]
    while True:
      q = sorted(list(more)) + q
      more.clear()
      if len(q) == 0: break
      v = q.pop(False)
      if v in done: continue
      done.add(v)
      for w,p in adj[v].iteritems():
        if w in tree: continue
        more.add(w)
        tree[v].add((w,p))
        tree[w].add((v,adj[w][v]))

print_tree(tree)