import networkx as nx
from tncontract import *
import numpy as np

class TensorNetwork(nx.Graph, Tensor):
    
    def __init__(self, tensorarray, index_pairs):
        """
        Attributes
        ----------
        
        tensorarray: a list consisting of Tensor objects
        
        index_pairs: a list consisting of pairs of indices belonging to the tensors in tensorarray
        which are to be contracted to form the given tensor network. The pattern of index contractions
        will determine the adjacency structure of the graph.
        """
        if not isinstance(tensorarray, list):
            raise ValueError("tensorarray must be a list of tncontract.Tensor objects")
        
        if not all(isinstance(x, Tensor) for x in tensorarray):
            raise ValueError("All elements of tensorarray must be of type tncontract.Tensor")
            
        if not isinstance(index_pairs, list) and not all(isinstance(n, tuple) for n in index_pairs) \
                        and not all(len(n)==2 for n in index_pairs):
            raise ValueError("index_pairs must be a list whose each element is a tuple")
            

        self.tensors = {}
        
        nx.Graph.__init__(self)

        for i in range(len(tensorarray)):
            t_label = 'Tensor' + '_' + str(i)
#             t_label = tensorarray[i].__name__
            self.tensors[t_label] = tensorarray[i]
            self.add_node(t_label, tensor=tensorarray[i], degree=len(tensorarray[i].labels))
            
        for (k,v) in self.tensors.items():
            print(k, v.labels)
            
        self.index_dict = {}
        
        index_list = []
        
        self.contracted_index_set = set()
        
        for (t_label, tensor) in self.tensors.items():
            for index in tensor.labels:
                self.index_dict[index] = t_label
            
            index_list.extend(tensor.labels)
                
        self.all_index_set = set().union(self.index_dict)

            
        if len(index_list) != len(self.all_index_set):
            raise ValueError("Duplicate index labels found. All tensor labels should be unique.")
            
        for (idx1,idx2) in index_pairs:
            if idx1 not in self.all_index_set or idx2 not in self.all_index_set:
                raise ValueError("The indices in the pair " + (idx1,idx2) + " must correspond to "\
                                 " the indices of some tensor(s)")
                
        idx3_list = []
        
        for idx_list in zip(*index_pairs):
            for x in idx_list:
                idx3_list.append(x)
                
        if len(set(idx3_list)) != len(idx3_list):
            raise ValueError("No index can occur more than once in the pairs of indices to be contracted")
            
        for (idx1, idx2) in index_pairs:
            
            print(idx1, idx2)
            
            t1 = self.index_dict[idx1]
            t2 = self.index_dict[idx2]
            
            if self.tensors[t1].index_dimension(idx1) != self.tensors[t2].index_dimension(idx2):
                raise ValueError("Dimension of index " + idx1 + " of tensor " + t1 + " does not match "\
                                 " dimensions of index " + idx2 + " of tensor " + t2)
            
            self.add_edge(t1,t2)
            
            self.contracted_index_set = self.contracted_index_set.union([idx1], [idx2])
            
            print(self.contracted_index_set)
            
        self.free_index_set = self.all_index_set.difference(self.contracted_index_set)
        
        print("All indices: ", sorted(self.all_index_set))
        print("Contracted indices: ", self.contracted_index_set)
        print("Free indices: ", self.free_index_set)
    
        Tensor.__init__(self,data=[])
    
#         Tensor.__init__(self, labels=self.contracted_index_set)
    
