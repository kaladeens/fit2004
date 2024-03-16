from typing import Any


class Graph:
    """
    Will represent a network which has maxIn and maxOuts.

    Attributes;
    source: the source of the array
    connections: the original inputted connections list
    targets: list of the targets 
    maxIn: list of the maximum flow in values
    maxOut: list of the maximum flow out values
    supersink: the id of the supersink
    length: the length of the adjacency list
    flow: an adjacency list which has the flows that are present in the network
    capacity: an adjacency list which has the capacities that limit the network
    """
    def __init__(self,connections: list,maxIn:list,maxOut:list,origin,targets):
        """
        initialises all the important attributes for the array

        time complexity: O(|C|*|D|)
        aux space complexity: O(|C|+|D|)
        """
        ## initalise with useful attributes
        self.source=origin
        self.connections=connections
        self.targets=targets
        self.maxIn=maxIn
        self.maxOut=maxOut
        self.supersink=None
        self.length=len(maxIn)*3+1
        self.flow=self.make_adjacency_list_with_max_in_and_out(connections,maxIn,maxOut,True)
        # print(self.flow)
        self.capacity=self.make_adjacency_list_with_max_in_and_out(connections,maxIn,maxOut)
        # print(self.capacity)
        
        #calling it 2 * so O(3(|C|*|D|)) -> O(|C|*|D|)

    def make_adjacency_list_with_max_in_and_out(self,graph: list,maxIn:list,maxOut:list,forFlow=False) -> list: 
        """
        Function Description: transforms the communication and maxes lists into an adjacency list representation
                              this representation will have extra edges which will represent the limits set by maxIn and maxOut
                              every maxIn will be the one that the other edges point to then that points to the id*3 then that points
                              to the maxOut which will then point to all the nodes this node can reach therefore abides by the bounds. 

        @param graph: a matrix representing the network
        @param maxIn: a matrix which has the maximum flow for an input to a vertex i
        @param maxOut: a matrix which has the maximum flow out for a vertex to go to another.
        @param forFlow: boolean value for whether we are building the flow diagram
        @return: the list representing the adjacency list

        time complexity: O(|C|+|D|+|C|*|D|) -> O(|C|*|D|) where D is the data centres (nodes) and C the communication channels (edges)
        aux space complexity: O(|C|+|D|) where D is the data centres (nodes) and C the communication channels (edges)
        """

        #for the max in and out thinking for every one there should be an edge to it with capacity of whatever, then itself,then capacity of it out to whichever node it can go to
        maximum=len(maxIn)
        adjacency_list=[]      
        for i in range((maximum*3)):       #time + aux space comp: O(|3*D|)->O(|D|)
            adjacency_list.append([])

        for communication_line in graph:  #loop through all edges and add  edge at 3 * its vertex id time + aux space comp O(|C|)      
            index=communication_line[0]*3+1
            goingTo=communication_line[1]*3
            throughput=communication_line[2]
            if forFlow:
                throughput=0
            adjacency_list[index+1].append([goingTo,throughput]) 
        #basically they increment by like the third element showing where next

        for i in range(len(maxIn)):      # this loop will add the limits for capacity in and capacity out time + aux space comp O(|D|)
            index=i*3
            if forFlow:
                adjacency_list[index].append([index+1,0])
                adjacency_list[index+1].append([index+2,0])
            else:
                adjacency_list[index].append([index+1,maxIn[i]])
                adjacency_list[index+1].append([index+2,maxOut[i]])
            
        self.add_super(adjacency_list,self.targets,forFlow)     #O(|C|*|D|)

        return adjacency_list
    
    def add_super(self,listChosen:list,targets:list,forFlow):
        """ 
        Function Description: This adds the supersink node to a list given some targets.

        @param listChosen: adjacency list to add the super sink to
        @param targets: list of the targets we want to go to
        @param forFlow: boolean value for whether we are building the flow diagram

        @postcondition listchosen now has a new superSink node

        time complexity: O(|C|*|D|) where D is the data centres (nodes) and C the communication channels (edges)
        aux space complexity: O(1) 
        """
        listChosen.append([])               # add the super sink node
        self.supersink=len(listChosen)-1
        
        for target in targets:              # go through the targets then find every node that can connect to it and add its capacity time comp O(|T|*|C|)
            temp_weight=0                                              #in worst case targets are |D|-1 size so time comp: O(|D|*|C|)
            for u,v,weights in self.connections:
                if v==target:
                    temp_weight+=weights+self.maxIn[v]+self.maxOut[v]
            if forFlow:
                temp_weight=0 
            
            for i in range(len(listChosen[target*3+1])):        # a target is just a target so it doesnt need the max out to limit it
                listChosen[target*3+1][i][1]=temp_weight
            listChosen[target*3+2].append([self.length-1,temp_weight])
            
    def BFS(self,preds:list):
        """ 
        Function Description: Does breadth first search on the graph to find a path returns True if path

        @param preds: a list of preds to change and store the previous nodes
        @return returns a bool of whether a path is available or not
        @postcondition preds has the path from th supersink to the source if there is a path available

        time complexity: O(|C|+|D|) where D is the data centres (nodes) and C the communication channels (edges)
        aux space complexity: O(|D|) where D is the data centres (nodes) and C the communication channels (edges)
        """
        visited=[False]*self.length     #size of data centres
        queue=[self.source*3 +1]        #size of data centres
        while len(queue)>0:             #will occur O(|D|) times as will always add an unvisited node
            u=queue.pop(0)
            for i in range(len(self.flow[u])):  #will occur through all edges so time O(|C|) all together
                v=self.flow[u][i][0]
                if not visited[v] and self.flow[u][i][1]<self.capacity[u][i][1]:
                    visited[v]=True
                    queue.append(v)
                    preds[v]=(u,i)
                    if v==self.supersink:
                        return True
        return False


def maxThroughput(connections: list,maxIn:list,maxOut:list,origin:int,targets:list)->int:
    """
    Function Description:  find the max throughput from the list of data centres and their connnections given their max for in and out

    function approach: I wanted to make an adjacency_list representation of the graph so I can work with it as I am most familiar with this representation,
    I also wanted to use them for some bfs so i made a graph class which will group the attributes I will use as well as some useful methods e.g. self.BFS.
    This makes the first step be to make the graph so we can have this useful object.
    I then wanted to start using the Edmond Karp method to augment the flow and find the maxThroughPut.
    The next portion does a BFS where we will pass the path on to the preds list, the BFS will search through edges and add them as a valid path if the flow
    through it is less than the capacity as that means we will be able to augment it and its not at its max flow already.
    The BFS will cause the algorithm loops over maximum times the amount of edges as we will cut off one path each time when we augment.
    If there is a path then we will find the maximum flow we can add to this path and add that to 
    the maximum throughput. We then update all the flows we have augmented. Then return the maxThroughput.
    --------------------------------------------------------------------------------------------------------------------------------------------------------------
    For the creation of the graph we at most will have to go through the list of data centre against the list of communication channaels in the case where
    the targets are essentially the size of data centres this means constructing them is costing O(|D|*|C|) time and O(|C|+|D|) aux space   

    within the main function we will go over a loop for as long as there is a valid path, this will occur O(|C||D|) times as we will cut off one edge from the 
    graph each time when we augment hence cutting off a path to the supersink however it may still become critiscal therefore the complexity, this BFS search also 
    costs O(|C|+|D|) we also loop over the length of the data centres as we augment the flow and update their current flow, 
    hence time comp is O(|C||D|*(|C|+|D|+|D|)) -> O(|C|^2 *|D|)
    the aux space comp here is O(|D|) as we only make a new preds list of size data centres
            
    --------------------------------------------------------------------------------------------------------------------------------------------------------------

    @param graph: a matrix representing the network
    @param maxIn: a matrix which has the maximum flow for an input to a vertex i
    @param maxOut: a matrix which has the maximum flow out for a vertex to go to another.
    @param origin: the id of the source data channel (vertex)
    @param targets: list of the targets we want to go to
    @return: the maximum throughput which can be sent to the targets

    time complexity: O(|C|^2 *|D|) where D is the data centres (nodes) and C the communication channels (edges)
    aux space complexity: O(|C|+|D|) where D is the data centres (nodes) and C the communication channels (edges)
    """
    
    
    graph = Graph(connections,maxIn,maxOut,origin,targets)  #create a graph object from the inputted paramaters time O(|D|*|C|)
                                                                                                        #aux space O(|D|+|C|)
    
    throughPut=0
    preds=[None] * graph.length             #initialise preds to be none ye aux O(|D|)
    #Loop will occur as long as there is a path from source to super sink and as we cut off at least one path to supersink each time 

    while graph.BFS(preds):         #O(|C|+|D|) for this operation

        if preds[graph.supersink] is None:  #if for some reason predsof supersink is none terminate
            break
        searching_flow=float("inf") 
        current_flow=float("inf")       #set these to infinite
        v = preds[graph.supersink]

        while v is not None:            #goes through the preds which could be O(|D|) worst case
            index=v[1]
            node=v[0]
            current_flow=graph.capacity[node][index][1]-graph.flow[node][index][1]
            searching_flow=min(searching_flow,current_flow)
            v=preds[node]

        throughPut+=searching_flow

        v=preds[graph.supersink]
        while v is not None:            #goes through the preds which could be O(|D|) worst case
            index=v[1]
            node=v[0]
            graph.flow[node][index][1]+=searching_flow   
            v=preds[node]
        
        preds=[None]* graph.length
    #O(|D|*|C|^2)

    return throughPut




class CatNode:
    """a class to represent the nodes of the trie

    Attributes;
    char: the character of the node
    child_array: the child_array of this node
    frequency: the frequency of this string occuring present at terminating character 
    highest_frequency: the highest frequency of the occurences of the words ending below it
    
    """
    def __init__(self,character) -> None:
        """initialised a node with char character
        @param character: the character we are adding

        time comp:O(1)
        space comp: O(ALPHABET_SIZE)
        """
        self.char = character
        self.child_array = [None]*27
        self.frequency=0
        self.highest_freq=0
    def __repr__(self) -> str:
        return str(self.highest_freq)
# The CatsTrie class structure
class CatsTrie:
    """a class representing a prefix trie data struture made up of catNodes

    Attributes;
    sentences: the list of sentences we will make
    root: the root of the trie

    """
    def __init__(self, sentences):
        """
        initialises the trie based on sentences

        @param sentences: the list of words we will be adding to the trie

        time comp: 
        aux space comp:
        """
        self.sentences=sentences
        self.root=CatNode(None)
        self.initialise_trie()

    def initialise_trie(self) -> None:
        """
        function description: goes through all words in the sentence and adds them to the trie
        
        @postcondtion all words in sentence are added to the trie

        time comp: O(N*M) where N is the amount of words in sentences and M the length of the longest word
        """
        for word in self.sentences: #occurs N times 
            self.insert(word)       #time comp is O(M)
        self.update_max_frequencies()
        

    def insert(self,word:str) -> None:
        """
        function description: insert a word to the prefix tree stemming from the root

        @param word: the word we are inserting to the trie

        time comp: O(M) where M is the length of the word
        aux space comp: O(26*M)->O(M) where M is the length of the word
        """

        node=self.root                  # start at root
        word="".join([word,'{'])        # time comp: O(M)
        arr=node.child_array            #get child array

        for c in word:                  # go down array and find index and insert there
            index = self.get_index(c)   # if there is no node there then add a new one else just move onto the next one
            if arr[index] is None:
                newNode = CatNode(c)
                arr[index] = newNode
            else:
                newNode = arr[index]  
            arr = newNode.child_array
        newNode.frequency+=1            # increment frequency at the terminating character

    def get_index(self,c) -> int:
        """
        @param c: the character we want index of
        @return the index of that character for out catNode arrays

        time comp: O(1)
        aux space comp: O(1)
        """
        return ord(c)-97

    def update_max_frequencies(self):
        """function to call upon the aux recursive function 

        @postconditions the highest frequencies of all catnodes in trie wil now be updated with valid values.
        
        time comp: O(N*M) where N is the amount of strings and M the length of the longest
        aux space comp: O(M) as depth of recursion is the length of M which is the longest string
        """
        node=self.root
        return self.update_aux(node)
    
    def update_aux(self,node:CatNode):
        """function will go down till the bottom node, terminating character, and return up the max indexes and update the highest frequencies of the nodes above
        
        @param node: the node we are currently at
        
        time comp: O(N*M) where N is the amount of strings and M the length of the longest
        aux space comp: O(M) as depth of recursion is the length of M which is the longest string
        """
        max_frequency=0
        for i in range (27): ##go through each position in array and go down if not none and get that max freq
            if node.child_array[i] is not None:
                max_frequency=max(max_frequency,self.update_aux(node.child_array[i]))
        if node.char=="{":  #base case 
            return node.frequency
        node.highest_freq=max_frequency #set to this on way back up
        return max_frequency
    

    def autoComplete(self, prompt:str)->str:
        """ 
        autocomplete for a given prefix

        function approach:
        first just wanted frequencies at the terminating character then would get each word from the trie which has the prefix prompt, then compare and get
        minimum, This proved to work but was out of complexity bounds, therefore I attampted to use the property of a trie already beingin alphabetical order.
        this was achieved by looping from the start and adding a new highest _frequency to the catNode to see if a path was worth searchin or not, this meant we 
        weould not have Y be the longest string but instead just the most frequent as we will disregard longer unless it has more frequent appearances.
        Also we would check if there were any more improvements in the highest frequency and if not we would terminate at that cjaracter which meant we would not keep
        searching even if there was another with the same max but was a higher index thus not in alphabetical order.
        --------------------------------------------------------------------------------------------------------------------------------------------------------------
        the complexity of join is O(n) where n is the length of the total output

        the complexity of get_max is O(1) as the alphabet size is a constant O(26) -> O(1)

        the complexity of search is O(M) where M is the length of the word to search for, as we will go down the trie till we find it which wil
        occur M times if it is in it.

        This algorithm itself also goes over the prefix provided to see how far we can go in trie O(X) from there it checks the most frequent nodes 
        which are next and picks them therefore only does the most frequent words so O(Y) time complexity where Y is the length of the most frequent 
        word with prefix prompt as we would terminate if no more frequent characters.
        --------------------------------------------------------------------------------------------------------------------------------------------------------------

        @param prompt: the prefix we are tryingt to find the autocompleted version of from trie
        @return the string of the autocompleted word from trie

        time comp: O(X+Y) where X is the length of the prompt and Y is the length of the most frequent word which has the prompt as a prefix
        """
        node = self.root
        arr=node.child_array
        
        search=self.search(prompt)                       #searched if prefix in word and if it is then check if it has max_frequency 
        if search[0] and search[1]>=self.get_max(arr,0)[1]: #if so then return prompt as autocomplete
            return prompt
        
        for c in prompt:            #goes over the length of the prompt O(X)
            index=self.get_index(c)
            node=arr[index]
            if node is None:
                return None
            arr=node.child_array
        
        arr=node.child_array
        old=node.highest_freq
        new_str=[]

        while node.char !="{":
            index=self.get_max(arr,old)[0]
            if index==26 or arr[index] is None:                   #if index is a terminating character then finish or if the node is none then we are done
                break
            node=arr[index]
            new_str.append(node.char)           #O(1) append
            arr=node.child_array
        new_str="".join(new_str)            #O(Y) join
        return "".join([prompt,new_str])    #O(Y) join
        
    
    def search(self,word: str) :
        """
        searches if the word is in the trie

        @param word: the word we are searching for
        @return a tuple containg a bool of whether the word is in and the frequency of the word

        time comp: O(M) where M is the length of the word
        space comp: O(1) 
        """
        node=self.root              #start from root
        word="".join([word,'{'])
        for c in word:              #loop through length of the word O(M)
            arr=node.child_array
            index = self.get_index(c)
            if arr[index] is None:
                return (False,0)
            if index == 26:         #return true if char found
                node=arr[index]
                return (True,node.frequency)
            node=arr[index]
        return (False,0)
        
    def get_max(self,arr:list,old_max):
        """
        gets the maximum index from the child array and returns its index or the terminating character if done
       
        @param arr: the list we will be searching through 
        @param old_max: the max of the parent 
        @return the index of the maximum element or the terminating character if finished

        time comp: O(1) as we only go through the list of alphabet size which is constant 
        aux space comp: O(1) nothing added
        """
        max=0
        max_ind=0
        for i in range (27):                #goes through the array and checks each one for the highest frequency to try update the max
            if arr[i] is not None and arr[i].highest_freq>max:
                max = arr[i].highest_freq
                max_ind=i
        if max<old_max and arr[-1] is not None: #if the max is less than old_max then where we are at is the best word so return 26 to terminate
            return (26,max)
        if arr[-1] is not None and arr[-1].frequency==max:  #if frequency is equal to the max and we can terminate then return 26 to terminate
            return (26,max)

        return (max_ind,max)
       
