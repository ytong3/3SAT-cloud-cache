import dbHelper

DEBUG = True
    
def log(s):
    if DEBUG:
        print s
class Solver:
    def __init__(self):
        "connect the solver to the default database"
        self.db = dbHelper.database()
       
    def recursionSolve(self, VarNum, problem_list):
        
        #base case for recursion
        #if less than 20clauses, then solve the problem by brute-force
        #rewrite the proList to problemList, which is a list of clauses
        # TODO input error checking
        if len(problem_list)<=3*3:
            result = self.db.dbQuery(self.problemListToString(problem_list))
            if result==None:
                result = self.bfSolver(VarNum, problem_list)
                self.db.dbStore(self.problemListToString(problem_list), self.solListToString(result))
            else:
                print "cache hit"
                result = self.solStrToList(result)
                
            #and insert the solution(string) to the database
            return result
        
        result = self.db.dbQuery(self.problemListToString(problem_list))
        if not result == None:
            log('cache used')
            return self.solStrToList(result)
                                 
        #divide the problem_list into two halves and check if they share the same solution
        midLength = (len(problem_list)/3)/2
        midLength = midLength*3-1
        #check if the first half is already solved
        #l_result = self.db.dbQuery(self.problemListToString(problem_list[0:midLength+1]))
        #if a solution is returned, just keep it.
        #if not recursionSolve the problem
        #make sure that l_result is a list of numbers
        l_result = self.recursionSolve(VarNum, problem_list[0:midLength+1])
        
        #if l_result == None:
        #    l_result = self.recursionSolve(VarNum, problem_list[0:midLength+1])
        #else:
        #    #cache hit
        #    print("cache hit")
        #    l_result = self.solStrToList(l_result)
         
        r_result = self.recursionSolve(VarNum, problem_list[midLength+1:])        
        #check if the second half is already solved
        #r_result = self.db.dbQuery(self.problemListToString(problem_list[midLength:]))
        #if r_result == None:
        #    r_result = self.recursionSolve(VarNum, problem_list[midLength+1:])
        #else:
        #    print("cache hit")
            #caches hit
        #    r_result = self.solStrToList(r_result)
        
        #check if the left and the right dovetail
        result=''
        if l_result == 'False' or r_result == 'False':
            result = 'False'
        elif l_result==r_result:
            #print "cache used"
            result=l_result
        else:
            result=self.bfSolver(VarNum,problem_list)
        
        #cache the result into the database
        self.db.dbStore(self.problemListToString(problem_list),self.solListToString(result))
        
        return result
        
        
    
    def problemStrToList(self,problem_str):
        "Convert a problem string, e.g. '12,-13,24,1,4,-1' to a problem list, e.g. [12,-13,24,1,4,-1]"
        proList = problem_str.split(',')
 #       while idx<len(problem_str):
#            clause=""
#            for i in xrange(3):
  #              if problem_str[idx]=='-':
   #                 clause=clause+problem_str[idx:idx+2]
    #                idx=idx+2
     #           else:
      #              clause=clause+problem_str[idx]
       #             idx=idx+1
        #    to_return.append(clause)
        return proList
    
    def problemListToString(self,problem_list):
        to_return=''
        for item in problem_list:
            to_return=to_return+','+str(item)
        return to_return
        
    def solListToString(self,problem_list):
        if problem_list == 'False':
            return 'False'
        
        to_return=''
        for item in problem_list:
            to_return=to_return+str(item)
        return to_return
    
    def solStrToList(self,problem_str):
        if problem_str =='False':
            return problem_str
        return [int(x) for x in problem_str]
        
    def bfSolver(self,VarNum, problem_list):
        #enumerate though all possible solutions
        #make sure that the number of variables in problem_str is consistent with
        log("searching solution for problem"+str(VarNum)+str(problem_list)) 
        bitmap = 1<<VarNum
        bitmap = bitmap-1
        while bitmap>=0:
            #sol is represented by list
            sol=[]
            for i in xrange(VarNum):
                sol.append((bitmap>>i)%2)
            if self.solTest(problem_list,sol):
                return sol
            else:
                bitmap=bitmap-1
        return 'False'
    
    def solTest(self,problem_list,sol):
        "sol is a list of 0's and 1's"
        idx = 0
        
        while idx<len(problem_list):
            #get the value of the clause beginning at idx
            clause =[]
            for i in xrange(3):
                clause.append(self.getValueBySymbol(problem_list[idx+i], sol))
            
            idx = idx+3
            
            if(not (clause[0] or clause[1] or clause[2])):
                return False
            
        return True
      
    def getValueBySymbol(self,symbol,sol):
        #log(symbol)
        if symbol[0]=='-':
            return not sol[int(symbol[1:])-1]
        else:
            return sol[int(symbol)-1]


#mysolver = Solver()
#mysolver.recursionSolve(4, ['-1','-2','-1','3','-2','1','-4','-2','1','2','3','4','4','1','3'])
