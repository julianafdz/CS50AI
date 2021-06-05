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
        for v in self.crossword.variables:
            delete_words = []
            for word in self.domains[v]:
                if len(word) != v.length:
                    delete_words.append(word)
            for del_word in delete_words:
                self.domains[v].remove(del_word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlaps = self.crossword.overlaps[x, y]
        revision = False
        if overlaps is None:
            return revision
        temp_dom_x = self.domains[x].copy()
        for word_x in temp_dom_x:
            match_checker = False
            for word_y in self.domains[y]:
                if word_x[overlaps[0]] == word_y[overlaps[1]]:
                    match_checker = True
            if match_checker is False:
                self.domains[x].remove(word_x)
                revision = True

        return revision            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = arcs
        if queue is None:
            queue = []
            for v in self.crossword.variables: 
                for neighbor in self.crossword.neighbors(v):
                    new_arc = (v, neighbor)
                    queue.append(new_arc)
        while queue:
            arc = queue.pop(0)
            x, y = arc[0], arc[1]
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in (self.crossword.neighbors(x) - {y}):
                    queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if self.crossword.variables != set(assignment.keys()):
            return False
        for var in assignment:
            if not assignment[var]:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = assignment.values()
        if len(values) != len(set(values)):
            return False
        for var1 in assignment:
            if len(assignment[var1]) != var1.length:
                return False
            for var2 in assignment:
                if var1 != var2:
                    overlaps = self.crossword.overlaps[var1, var2]
                    if overlaps:
                        if assignment[var1][overlaps[0]] != assignment[var2][overlaps[1]]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        temp_dict = {}        
        for word in self.domains[var]:
            num_of_ruledout = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment.keys():
                    if word in self.domains[neighbor]:
                        num_of_ruledout += 1
            temp_dict[word] = num_of_ruledout
        temp_list = list(temp_dict.items())
        temp_list.sort(key=lambda num: num[1])
        final_list = []
        for value in temp_list:
            final_list.append(value[0])
        return final_list            

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = list(self.crossword.variables - set(assignment.keys()))
        unassigned_vars.sort(key=lambda var: len(self.domains[var]))
        min_dom_var = unassigned_vars[0]
        list_min_vars = []
        for var in unassigned_vars:
            if len(self.domains[min_dom_var]) == len(self.domains[var]):
                list_min_vars.append(var)
            else:
                break
        if len(list_min_vars) > 1:
            list_min_vars.sort(key=lambda var: len(self.crossword.neighbors(var)), reverse=True)
            max_degree_var = list_min_vars[0]
            return max_degree_var
        else:
            return min_dom_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        return None


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
