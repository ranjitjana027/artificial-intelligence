import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for key in self.domains:
            self.domains[key]={x for x in self.domains[key] if len(x)==key.length}

        #print("After Enforcing Node Consistency: ", self.domains)
        #raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #print(self.crossword.overlaps[x,y])
        removed=set()#{k for k in self.domains[x] if len(self.domains[y]-{k})==0}
        for val in self.domains[x]:
            satisfied=False
            for k in self.domains[y]-{val}:
                if self.crossword.overlaps[x,y]:
                    xpos,ypos= self.crossword.overlaps[x,y]
                    if val[xpos]==k[ypos]:
                        satisfied=True
                        break
                else:
                    satisfied=True
                    break
            if not satisfied:
                #print(val," ",self.crossword.overlaps[x,y])
                removed.add(val)



        self.domains[x]-=removed
        return len(removed)!=0 
        #raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs=[(k1,k2) for k2 in self.domains for k1 in self.domains if k1!=k2]
        while len(arcs)!=0:
            x,y=arcs.pop(0)
            if self.revise(x,y):
                if len(self.domains[x])==0:
                    return False
                for z in self.domains:
                    if z!=x:
                        arcs.append((z,x))

        #print(self.domains)
        #raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment)==len(self.domains)
        #raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        vals=set([assignment[key] for key in assignment])
        if len(vals) != len(assignment):
            return False
        for k1 in assignment:
            for k2 in assignment:
                if k1!=k2:
                    if self.crossword.overlaps[k1,k2]:
                        pos1, pos2=self.crossword.overlaps[k1,k2]
                        if assignment[k1][pos1]!=assignment[k2][pos2]:
                            return False

        return True
        #raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #return list(self.domains[var])
        return sorted(self.domains[var], key=lambda v: self.heuristic(var,v,assignment))
        #raise NotImplementedError

    def heuristic(self,var,val,assignment):
        i=0
        for key in self.domains:
            if var!=key and key not in assignment:
                for v in self.domains[key]:
                    if v==val:
                        i+=1
                    elif self.crossword.overlaps[var,key]:
                        x1,x2=self.crossword.overlaps[var,key]
                        if val[x1]!=v[x2]:
                            i+=1
        return i


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_domain=None
        highest_degree=-1
        var=None
        for key in self.domains:
            if key not in assignment:
                count=self.crossword.neighbors(key)
                """for k in self.domains:
                    if k!=key and self.crossword.overlaps[key,k]:
                        count+=1"""
                if  min_domain is None or min_domain>len(self.domains[key])  or ( min_domain==len(self.domains[key]) and ( count>highest_degree or ( count==highest_degree and key.length<var.length) )):
                    min_domain=len(self.domains[key])
                    highest_degree=count
                    var=key
               
        return var             
        #raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #print(len(assignment))
        if self.assignment_complete(assignment):
            return assignment
        
        var =self.select_unassigned_variable(assignment)
        #print(var)
        for value in self.order_domain_values(var,assignment):
            #print(value)
            assignment[var]=value
            if self.consistent(assignment):
                self.ac3([(k,var) for k in self.domains if k!=var])
                result=self.backtrack(assignment)
                if result:
                    return result
            assignment.pop(var)
        return None
        #raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
