import heapq

def optimalRoute(start:int, end:int ,passengers:list, roads:list)->list:
    """
    Function decription: finds the most optimal path in a list of roads with carpool and singular paths, this then returns the list of 
    this path.


    function approach: I first wanted arrays with each one corresponding to a node so i could look up in O(1)
    I also implemented the algorithm with a queue so i can use this greedy algorithm and have the best update and pop complexities O(log|L|).
    This queue would work even without having a another vertex array to keep track of its position as we would disreagard the value popped if it was
    not equal to the current estimate we had for it and not involved in a passenger calculation.
    for the inside of the while loop it worked by first getting the shortest distance in queue currently and then first checking if their 
    is a passenger, if there isnt it will try relax the node as it loop through the edges it is connected to. if there is a passenger 
    then pick them up because it will always improve or keep time the same, then let it try to relax it against the distances or passenger_dist as
    distances could be ahead, this allows it to stay in queue, thus allowing the passenger route to be searched we would also pass on whether or not it had
    a passenger so we could determine what to check it against.
    For these passenger routes where distance[with_passneger] is not less than the actual weight it will go through the carpool lanes and 
    update passenger_dist exclusively until it is a better option than what was in distances before.
    This enables the algorithm to be correct whether a passenger coming helps or not as it will not terminate until those paths have been completed
    as well and reflected in the arrays.
    The path finding was done by going through the passenger_dist first, if valid, then the singular distances one. This would 
    get the full path even when there was no passenger picked up, we would also keep track of the index because when they align it means thats where we picked up
    so thats where we go into the singular distances loop.
    We then return this finished path.
    -----------------------------------------------------------------------------------------------------------------------------------

    given L is the list of key locations and R the roads list:

    the make_adjacency_list function costs O(|L|+|R|) time and aux space as we make a new list of the vertices and edges assosciated with.

    the dijiksrata_algo function costs O(|P|log|L|+|R|log|L|+|L|log|L|+|L|+|P|) time as we pop and push from the queue hence adding log|L| complexity and as we have to 
                                                            push further O(|P|) times on top of regular O(|R|) this also means we pop it more but does not change complexity
                                                            as the term that dominates is the |R|log|L| as |R| >= |L| > |P|
                                                            therefore time complexity is: O(|R|log|L|)
                                the algo costs O(|L|) aux space complexity as we only add arrays of size |L| 

                                the traceback function does not add to any of the complexities at O(|L|) aux space and time
    -----------------------------------------------------------------------------------------------------------------------------------

    @param start: integer of the starting node.
    @param end: integer of the ending node
    @param passengers: the list of nodes where passengers can be picked up
    @param roads: a list of tuples representing the roads
    @return the most optimal path, fastest route, from start to end

    time complexity: O(|L|+|R|+|R|log|L|) -> O(|R|log|L|)
    space complexity: O(|L|+|R|+|L|) -> O(|L|+|R|)
    
    """
    
    adjacency_list = make_adjacency_list(roads)                     #time: and space = O(|L|+|R|)
    output = dijisktra_algo(adjacency_list,start,end,passengers)    #time: O(|R|log|L|) space: O(|L|)
    
    return output
    
def make_adjacency_list(graph: list) -> list: 
    """
    Function Description: transforms the roads graph into an adjacency list and returns said adjacency list.

    @param graph: a matrix representing the road
    @return: the list representing the adjacency list

    time complexity: O(|L|+|R|) where L is the key locations (nodes) and R the roads (edges)
    aux space complexity: O(|L|+|R|) where L is the key locations (nodes) and R the roads (edges)
    """

    maximum=0
    for road in graph:          #time comp: O(|R|) 
        if road[0]>maximum:     #finding max
            maximum=road[0]
        elif road[1]>maximum:
            maximum=road[1]
   
    adjacency_list=[] 
    for i in range(maximum+1):      #time + space comp: O(|L|)
        adjacency_list.append([])   #make empty lists within adjacency list  
                                
    for road in graph:          #time comp: O(|R|) 
        vertex=road[0]          #adding edges to the list of vertices
        el1=road[1]
        el2=road[2]
        el3=road[3]
        adjacency_list[vertex].append((el1,el2,el3))

    return adjacency_list

def dijisktra_algo(adjacency_list: list, source: int, end: int, passengers: list):
    """
    Function description: runs dijisktras algorithm to find the most efficient route from a source to a single target. takes into account the 
    passenger and the car pool lanes too, then returns this route

    @param adjacency_list: the adjacency list represnentation of the graph
    @param source: integer of the starting node.
    @param end: integer of the ending node
    @param passengers: the list of nodes where passengers can be picked up

    @return the most optimal path, fastest route, from start to end
    time complexity: O(|L|+|P|+|L|log|L|+|P|log|L|+|R|log|L|) --> O(|R|log|L|) as R >= L-1 > P. 
                                                         Where L is key locations and P passenger list and R the roads

    aux space complexity: O(|L|+|P|) -> O(|L|)  where L is the key locations, P the passenger list 
    """
    n=len(adjacency_list)
    distances = [None] * n
    pBool=[False] *n
    passenger_dist=[None] *n
    pred=[None]*n
    pred_passeng=[None]*n
                                #initialise the lists of size O(|L|) (nodes)
                                #space_comp=O(|L|)
    
    for i in range(n):          #space: O(2*|L|)->O(|L|) L is key locations (nodes)
        inf=float("inf")        #time: O(|L|)
        distances[i]=inf
        passenger_dist[i]=inf
  
    for num in passengers:      #space: O(|P|) P is array of passengers
        pBool[num]=True         #time: O(|P|)

    distances[source]=0
    
    queue=[(0,source,pBool[source])]        #distance,vertex,has_passenger stored within each queue item
                                            # in this queue item the max length will be O(1)*C

    ##Loops over the length of queue and pops each time which will be O(|L|log|L|) 
    while len(queue)>0:

        dist, vertex, has_passenger = heapq.heappop(queue)  #pop is O(log(|L|)) 
        
        if vertex==end:
            continue              
        # if it is at end then dip
            
        if dist<distances[vertex] and not has_passenger :
            continue
        #if its an old value then get rid of it unless it is involved in a passenger calc
        
            
        if pBool[vertex]:       #check if it has a passenger and store where we picked it
            has_passenger=True
            picked_index=vertex 
        
        for next_node, single_weight, pass_weight in adjacency_list[vertex]:        #loop TOTALS at all edges and whenever it adds a passenger so is of O(|R|+|P|) |P|<|R| and pushes to queue therefore O(|R|log|L|)
            if has_passenger:
                if dist+pass_weight<distances[next_node]: 
                    
                    try:                                                    #try update the index to the one from before in passenger 
                        if pred_passeng[vertex][1] is not None:             #if not then just use the new one as this is first pick up
                            picked_index=pred_passeng[vertex][1]
                    except TypeError:
                        pass

                    pred_passeng[next_node]=(vertex,picked_index)           #update passenger predecessors with the index of pick up aswell
                    distances[next_node]=dist+pass_weight                   #relax node
                    passenger_dist[next_node]=dist+pass_weight

                    heapq.heappush(queue,(distances[next_node],next_node,has_passenger))       #PUSH OPERATIONS ARE O(log(|L|))
                
                elif dist+pass_weight<passenger_dist[next_node]:
                    
                    try:                                                    #try update the index to the one from before in passenger 
                        if pred_passeng[vertex][1] is not None:             #if not then just use the new one as this is first pick up
                            picked_index=pred_passeng[vertex][1]
                    except TypeError:
                        pass

                    pred_passeng[next_node]=(vertex,picked_index)           #update passenger predecessors with index of pick up aswell
                    passenger_dist[next_node]=dist+pass_weight              #relax node
                    
                    
                    heapq.heappush(queue,(passenger_dist[next_node],next_node,has_passenger))  #PUSH OPERATIONS ARE O(log(|L|))
            
            else:
                if dist+single_weight<=distances[next_node]:            #if improves distance estimate
                    
                    distances[next_node]=dist+single_weight             #relax node
                    pred[next_node]=vertex                              #update pred
                    heapq.heappush(queue,(distances[next_node],next_node,False))   #PUSH OPERATIONS ARE O(log(|L|))
        
    
    #let me know if any passengers here
    if len(passengers)==0:  
        pass_bool=False
    else: 
        pass_bool=True

    #check if passenger route is faster
    skip_pass=False
    if passenger_dist[end]>distances[end]:
        skip_pass=True
   
    #call traceback method to get the route, time and space O(|L|) 
    path=traceback(pred,pred_passeng,end,source,pass_bool,skip_pass)

    return path
    
def traceback(preds:list, preds_passen:list, n:int, start:int ,passengers:bool, skip_pass:bool)->list:
    """
    Function Description: returns an array of the shortest path, searching through the predecessors arrays
    
    @param preds: an array of predecessors to non passenger ways
    @param preds_passen: an array of predecessors and pickup locations for when a passenger is in
    @param n: the integer index of the final node
    @param start: the integer index of start node
    @param passengers: bool of if there is a passenger
    @paran skip_pass: bool which is true if you should skip the passenger
    @return: a list of the full path till the final node with the shortest distance
    
    time complexity: O(|L|) where L is the key locations
    aux space complexity: O(|L|) where L is the key locations 
    """
    
    ouptut_path=[n]
    if not skip_pass:           #skip if without passengers is faster
        try:                                            #ensures that we only care about passengers that are in our route and ignores those out of bounds
            if passengers:                              #only runs if there is a passenger route:
                while preds_passen[n][0] is not None and n!=preds_passen[n][1]:   #backtracks until we find where the passenger hops on or until we reached source
                    ouptut_path.append(preds_passen[n][0])
                    n=preds_passen[n][0]                             
        except TypeError:
            pass
    
    while preds[n] is not None and preds[n]!=start:       #backtracks the other predecessors nodes from before we picked up passenger if necessary
        ouptut_path.append(preds[n])
        n=preds[n]    

    if ouptut_path[-1]!=start:                  
        ouptut_path.append(start)               
   
    ouptut_path.reverse()                       # reverses list O(|L|)

    return ouptut_path


def select_sections(occupancy_probability: list[list]) -> list:
    """
    Function Description: function to determine which sections we should remove to minimise the amount of space taken away as
                          according to the constraints 
                          1. have to be adjacent or itself
                          2. one section removed per row
    
    function approach: We first make a decision matrix which solves and stores all the subproblems, this was done in make_decision_matrix
    where it would go from the second row onwards and add the minimum of the adjacent columns in the row above, an optimisation done was adding the index 
    of the one above so that later when backtracking to find the most optimal solution it would not need to index the one above and could just go off
    of what it has stored lowering the time complexity of backtrack_occupancy from O(n*m) to O(n). There is also a case for the edge where if there
    is only one column where we just go straight down. we also ensure that we are within the adjacent columns by only regarding the adjacent ones in the 
    decision matrix instead of getting the min of each row, hence the edge cases for the sides.
    Once the decision matrix is made we can simply backtrack by getting min of the final row and following the indexes up till the first row. this is done in O(n)
    time by starting from the rear of the decision matrix, index -1, and going up through the index stored in the tuple. 

    ------------------------------------------------------------------------------------------------------------------------------------
    recurrence to construct optimal substructure, the decision matrix.
                      {occupancy_porbability[0][j]       for when i = 0     }  
                      {                                  {dec_matrix[i-1][j],dec_matrix[i-1][j-1]                for j=m-1}}
    dec_matrix[i][j]= {occupancy_probability[i][j] +  min{dec_matrix[i-1][j],dec_matrix[i-1][j+1]                  for j=0}}
                      {                                  {dec_matrix[i-1][j],dec_matrix[i-1][j+1], dec_matrix[i-1][j] else}}
    as for each entry in decision matrix we need the minimum of the adjacent ones above as well as the value of itself so this recurrence
    will work its way till the top where the base case occurs when i=0 where for each j it just equals itself in the occupancy matrix.
    ------------------------------------------------------------------------------------------------------------------------------------

    given n rows and m columns in occupancy_probability:

    make_decision matrix section costs O(n*m) time as we go through loop m n times
                                 and costs O(n*m) space , making the decision matrix
   
    backtrack_occupancy section costs O(n+m) as we go through all the rows however as 
                            n>m O(n+m) = O(n)
                            the space complexity is O(m*n + n) = O(m*n) as m*n dominates
    -----------------------------------------------------------------------------------------------------------------------------------

    @param occupancy_probability: an array of n rows and m columns containing occupancy probabilities 
    @return: the list containing the total_min_occupancy as well as the sections to be removed as tuples

    time complexity: O(n*m) 
    space complexity: O(n*m) 
    """
     
    n = len(occupancy_probability)                  #number of rows
    m = len(occupancy_probability[0])               #number of columns 
    
    dec_matrix=make_decision_matrix(occupancy_probability,n,m) #create the decision matrix aux space and time: O(n*m)

    output=backtrack_occupancy(dec_matrix,n,m)                 #creates the output by backtracking and returning indices time: O(n) and aux space:O(m)
   
    return output
    
def make_decision_matrix(occupancy_probability: list, n:int, m:int):
    """
    function description: build the decision matrix utilising the occupancy_probability and going down till bottom, this enables it to hold 
    the values of adding each one in the most efficient way.

    @param occupancy_probability: the array of occupancy probabilities for each section
    @param n: the integer representing the amount of rows in occupancy_probabilities
    @param m: integer representing the amount of colunns in occupancy_probabilities
    @return returns a decision matrix with the values of all the subproblems completed 

    time complexity: O(n*m)    where m is the columns and n the rows of occupancy_probability 
    space complexity: O(n*m)   where m is the columns and n the rows of occupancy_probability
    """

    dec_matrix=[]
    for i in range(n):
        dec_matrix.append([None]*m)                         #initialise decision matrix space comp: O(n*m)
   
    for j in range(m):                              
        dec_matrix[0][j] = (occupancy_probability[0][j],0)     #put first row as the original occupancy matrix with 0 attached
                                                   
                                                   
    for i in range(1, n):                           #bottoms up approach, building the decision matrix using the minimums time: O(n*m)
        for j in range(m):              # the min function is not O(m) as it only compares at most 3 values
            if m==1:
                minimum=dec_matrix[i-1][j][0]
                dec_matrix[i][j]=((occupancy_probability[i][j]+minimum),0)
            elif j == 0:                  #handling the edges
                minimum=min(dec_matrix[i-1][j][0], dec_matrix[i-1][j+1][0])
                if minimum==dec_matrix[i-1][j][0]:
                    index=j
                else: 
                    index=j+1
                dec_matrix[i][j] = ((occupancy_probability[i][j] + minimum),index)
            elif j==m-1:
                minimum=min(dec_matrix[i-1][j-1][0], dec_matrix[i-1][j][0])
                if minimum==dec_matrix[i-1][j][0]:
                    index=j
                else: 
                    index=j-1
                dec_matrix[i][j] = ((occupancy_probability[i][j] + minimum),index)
                
            else:                       #for when not on edge       
                minimum=min(dec_matrix[i-1][j-1][0], dec_matrix[i-1][j][0], dec_matrix[i-1][j+1][0])    #find minimum of above adjacent and then
                if minimum==dec_matrix[i-1][j][0]:                                                      #add the index to the one below 
                    index=j
                elif minimum==dec_matrix[i-1][j-1][0]: 
                    index=j-1
                else:
                    index=j+1
                dec_matrix[i][j] = ((occupancy_probability[i][j] + minimum),index)    
           
    return dec_matrix
   
def backtrack_occupancy(dec_matrix: list, n:int, m:int):
    """
    function description: function to backtrack and find the route from bottom till top which will get rid of the least used spaces 
                          whilst adhering to constraints.
    
    @param dec_matrix: matrix containing the values of the minimum occupancy rates for each index in occupancy_matrix
    @param n: the rows of dec_matrix
    @param m: the columns of dec_matrix
    @return returns a list which contains the minimum total occupancy rate and the tuples of which location should be removed per row

    time complexity: O(n+m) = O(n)  where n is the rows of dec_matrix
    space complexity: O(m*n + n) = O(m*n)  where m is the columns and n the rows of dec_matrix
    """

    min_occupancy = min(dec_matrix[-1])      #the final smallest occupancy
    minimum=min_occupancy[0]                 #O(m)
    
    sections_location = []                   #set up array of locations
    index=dec_matrix[-1].index(min_occupancy)    #add first index of minimum to array, this is beginning of backtracking O(m)
    sections_location.append((n-1,index))
    index=dec_matrix[-1][index][1]                   #get index for next

    for i in range(n-2, -1, -1):        #get min each time for range of n time : O(n) skip last row
        sections_location.append((i, index))    
        index=dec_matrix[i][index][1]           #set j to be the index we stored previously whilst the dec_matrix
        
    sections_location.reverse()             #reverse the list time: O(n)
    output=[minimum,sections_location]      #make output list

    return output   

