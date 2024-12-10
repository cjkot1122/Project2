class TuringMachine:
    def __init__(self, input):
        self.name = None
        self.tapes = []
        self.states = set()                 #machine parameters
        self.transitions = []
        self.num = 1
        self.heads = []
        self.curState = None
        
        self.parseInput(input)
    
    def parseInput(self, filename):
        with open(filename, 'r') as p:
            first = p.readline().strip().split()
            self.name = first[0]                                # parse line 1 and initialize tapes
            self.num = int(first[1]) if len(first) > 1 else 1     
            self.tapes = [list(p.readline().strip() + '_' * 100) for _ in range(self.num)]
            self.heads = [0] * self.num
            self.curState = None
            
            for line in p:
                transition = line.strip().split()         #then parse rest
                if not transition:
                    continue
                
                if self.curState is None:
                    self.curState = transition[0]

                expectedLength = 2 * self.num + 3       #update num of elements and check

                if len(transition) < expectedLength:
                    continue
 
                self.transitions.append(transition)                           #tracker
                self.states.update([transition[0], transition[self.num + 1]])

    
    def findMatches(self, curSyms):
        for transition in self.transitions:
            if transition[0] != self.curState:      #start check
                continue
            
            flag = True
            for i in range(self.num):
                inputSym = transition[i+1]
                if inputSym != curSyms[i] and inputSym != '*':    #checks for matches
                    flag = False
                    break
            
            if flag:
                return transition
        
        return None
    
    def simulate(self, total=800):
        with open('Outputs3.txt', 'w') as out:
            out.write(f"{self.name} Sim\n")      #output file setup
            
            for step in range(total):
                out.write(f"\nStep {step}:\n")
                curSyms = []
                
                for ind in range(self.num):         #syms
                    head = self.heads[ind]
                    tape = self.tapes[ind]
                    if head >= len(tape):
                        tape.extend(['_'] * (head - len(tape) + 1))   #extends tape (poss delete)
                    
                    curSym = tape[head]
                    curSyms.append(curSym)                #outputting
                    op = ''.join(tape)
                    out.write(f"Tape {ind+1}: {op[:head]} {op[head]} {op[head+1:]}\n")
                
                transition = self.findMatches(curSyms)    #call finder
                if transition is None:
                    break
                
                self.curState = transition[self.num + 1]   #state update
                
                for ind in range(self.num):
                    sub = transition[self.num + 2 + ind]        #tape update

                    if sub != '*':
                        self.tapes[ind][self.heads[ind]] = sub
                    
                    move = transition[2 * self.num + 2 + ind]

                    if move == 'R':                                     
                        self.heads[ind] += 1          #handle Left and Right
                    elif move == 'L':
                      self.heads[ind] = max(0, self.heads[ind] - 1)
                
                # final state check
                if self.curState in [x for x in self.states if x.startswith('qf')]:
                    out.write("halting, done\n")
                    break
            
            else:
                out.write("halting\n")


if __name__ == "__main__":
    tm = TuringMachine('Inputs3.txt')
    tm.simulate()
