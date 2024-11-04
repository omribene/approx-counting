from itertools import permutations 

all_patterns_4 = list(permutations(range(1, 5)))
all_patterns_5 = list(permutations(range(1, 6)))
all_patterns_6 = list(permutations(range(1, 7)))


class PatternWithSeparators(object):

    def __init__(self, pattern, main_separator, horizontal_separator=None, 
                 sub_separator=None, horizontal_sub_separator=None): 
        """
        pattern is a list of the values in the pattern. 
        For example (a 5-pattern): [1, 5, 3, 2, 4]

        main_separator is an index between 1 and (length of pattern - 1).
        It is placed right before the element at the same locations,
        where locations start with zero as is usual in python.

        horizontal_separator is a value between 2 and (length of pattern).
        It is placed under that value in the pattern.

        sub_separator params ended up being unused.
        """
        self.pattern = pattern
        self.length = len(self.pattern)
        self.main_separator = main_separator
        self.sub_separator = sub_separator
        self.vertical_separators = [sep for sep in (main_separator, sub_separator) if sep is not None]
        self.horizontal_separator = horizontal_separator
        self.horizontal_sub_separator = horizontal_sub_separator
        self.horizontal_separators = [sep for sep in (horizontal_separator, horizontal_sub_separator) 
                                      if sep is not None]
        self.fixed_locations = []
        self.fixed_values = []
        self.original_fixed_location = None
        self.original_fixed_value = None

    def __repr__(self):
        s = "".join([str(c) for c in self.pattern])

        if self.sub_separator is None:
            s = s[:self.main_separator] + "||" + s[self.main_separator:]
        else:
            if self.sub_separator < self.main_separator:
                s = s[:self.sub_separator] + "|" + s[self.sub_separator:self.main_separator] + "||" + s[self.main_separator:]
            else:
                s = s[:self.main_separator] + "||" + s[self.main_separator:self.sub_separator] + "|" + s[self.sub_separator:]

        if self.horizontal_separator is not None:
            s = s + " horizontal separator below value " + str(self.horizontal_separator)
            if self.horizontal_sub_separator is not None:
                s = s + " (main), " + str(self.horizontal_sub_separator) + " (sub)"
        
        return s
        
    
    
    def get_num_boundaries_single_element(self, i):
        """
        Returns the number of vertical and horizontal separators surrpounding 
        the element at location i of the pattern. This will be used to determine
        whether it can be fixed.
        """
        if i in self.fixed_locations:
            return 4

        num_borders = 0
        # separator / fixed element / border to the left?
        if i == 0 \
            or i in self.vertical_separators \
            or i-1 in self.fixed_locations:
            num_borders += 1
        
        # separator / fixed element / border to the right?
        if i == self.length - 1 \
             or i+1 in self.vertical_separators \
             or i+1 in self.fixed_locations:
             num_borders += 1
        
        val = self.pattern[i]
        # separator / fixed element / border below?
        if val == 1 \
        or val in self.horizontal_separators \
        or val - 1 in self.fixed_values:
            num_borders += 1

        # separator / fixed element / border above?
        if val == self.length \
        or val + 1 in self.horizontal_separators \
        or val + 1 in self.fixed_values:
            num_borders += 1

        return num_borders
    
    def get_num_boundaries_pair_elements(self, i):
        """
        Returns the number of vertical and horizontal separators surrpounding 
        a consecuitve monotone sequence at locations i,i+1 of the pattern. 
        This will be used to determine whether it can be fixed.
        """
        assert i < self.length - 1
        assert abs(self.pattern[i] - self.pattern[i+1]) == 1
        assert i not in self.fixed_locations and i+1 not in self.fixed_locations

        minval = min([self.pattern[i], self.pattern[i+1]])
        maxval = max([self.pattern[i], self.pattern[i+1]])

        num_borders = 0
        # separator / fixed element / border to the left?
        if i == 0 \
            or i in self.vertical_separators \
            or i-1 in self.fixed_locations:
            num_borders += 1
        
        # separator / fixed element / border to the right?
        if i+1 == self.length - 1 \
             or i+2 in self.vertical_separators \
             or i+2 in self.fixed_locations:
             num_borders += 1
        
        # separator / fixed element / border below?
        if minval == 1 \
        or minval in self.horizontal_separators \
        or minval - 1 in self.fixed_values:
            num_borders += 1

        # separator / fixed element / border above?
        if maxval == self.length \
        or maxval + 1 in self.horizontal_separators \
        or maxval + 1 in self.fixed_values:
            num_borders += 1

        return num_borders
        
    def fix(self, val):
        if val in self.fixed_values:
            return
        i = self.pattern.index(val)
        self.fixed_locations.append(i)
        self.fixed_values.append(val)
        if self.original_fixed_value is None:
            self.original_fixed_value = val
            self.original_fixed_location = i

    def auto_complete(self, debug_print = False):
        """
        After an initial element was fixed, this method tries to autocomplete
        the sequence of fixed elements, until ultimately all elements
        are fixed (or until it gets stuck).
        """
        fix_list = []
        while True:
            cont_flag = False
            for i in range(self.length):
                if i in self.fixed_locations:
                    continue
                if self.get_num_boundaries_single_element(i) >= 3:
                    self.fix(self.pattern[i])
                    if debug_print:
                        print("Fixed", self.pattern[i])
                    cont_flag = True
                if i < self.length - 1 \
                    and i not in self.fixed_locations \
                    and i+1 not in self.fixed_locations \
                    and abs(self.pattern[i] - self.pattern[i+1]) == 1 \
                    and self.get_num_boundaries_pair_elements(i) >= 4:
                    self.fix(self.pattern[i])
                    self.fix(self.pattern[i+1])
                    if debug_print:
                        print("Fixed", self.pattern[i], "and", self.pattern[i+1])
            if not cont_flag:
                return


def symmetry_groups(pattern_length):
    """
    Return all groups of patterns symmetric up to horizontal or vertical reflection
    for a certain pattern length.
    """
    all_patterns = list(permutations(range(1, 1+pattern_length)))
    groups = []
    for pattern in all_patterns:
        found = False
        for g in groups:
            if pattern in g:
                found = True
                break
        if not found:
            upside_down = tuple([pattern_length+1 - val for val in pattern])
            g_updown = [pattern,] if pattern == upside_down else [pattern, upside_down]
            g_leftright = [tuple(p[::-1]) for p in g_updown if tuple(p[::-1]) not in g_updown]        
            g = g_updown + g_leftright
            groups.append(g)
    return groups



def run(pattern, main_separator, horizontal_separator=None, try_sub_separator=True, 
        try_horizontal_sub_separator=False, debug_print=False):
    """
    Check for a given pattern and a single assignment of main (vertical) separator
    and an optional horizontal separator, whether there is a fixing sequence
    of the elements which leads to a near-linear algorithm.

    The sub_separator parameters are optional and have ended up not being analyzed
    in the paper (as they are not needed for 4-patterns, and do not suffice for
    capturing all 5-patterns).
    """
    win_flag = False

    pattern_str = "".join([str(c) for c in pattern])
    initial_state_string = pattern_str[:main_separator] + "|" + pattern_str[main_separator:]
    if horizontal_separator is not None:
        initial_state_string += ", horizontal below" + str(horizontal_separator)

    return_list = []

    for val in range(1, len(pattern)+1):
        if debug_print:
            print("Initially fixing", val)
        
        i = pattern.index(val)
        if try_sub_separator:
            vertical_sub_seps = range(1, main_separator) if i < main_separator \
                                 else range(main_separator+1, len(pattern))
        else:
            vertical_sub_seps = [None,]
        if try_horizontal_sub_separator and horizontal_separator is not None:
            horizontal_sub_seps = range(2, horizontal_separator) if val < horizontal_separator \
                                   else range(horizontal_separator+1, len(pattern)+1)
        else:
            horizontal_sub_seps = [None,]

        break_flag = False
        for ver_subsep in vertical_sub_seps:
            if break_flag:
                break
            for hor_subsep in horizontal_sub_seps:
                p = PatternWithSeparators(pattern, main_separator, 
                                          horizontal_separator=horizontal_separator,
                                          sub_separator=ver_subsep,
                                          horizontal_sub_separator=hor_subsep)
                p.initial_state_string = initial_state_string
                if debug_print:
                    print(p)
                p.fix(val)
                p.auto_complete(debug_print=debug_print)
                if len(p.fixed_values) != p.length:
                    break_flag = True
                    return_list = []
                    break
                p.fix_sequence = [str(p.fixed_values[0]),]
                if try_sub_separator:
                    p.fix_sequence.append("vertical between values" + str(pattern[ver_subsep-1]) + "&" + str(pattern[ver_subsep]))
                if try_horizontal_sub_separator:
                    p.fix_sequence.append("horizontal below value" + str(hor_subsep))
                p.fix_sequence += [str(c) for c in p.fixed_values[1:]]
                return_list.append(p)
        if break_flag is False:
            return True, return_list
    
    p = PatternWithSeparators(pattern, main_separator, horizontal_separator=horizontal_separator)
    p.initial_state_string = initial_state_string
    p.fix_sequence = ["FAILED",]
    return False, [p,]


def run_main_code(pattern_length, try_horizontal_separator=False, try_sub_separator=False, 
              try_horizontal_sub_separator=False, debug_print=False, output_path=None):
    """
    Check for all patterns of a given length whether they have a fix sequence.
    For each pattern and each vertical (+ possibly horizontal) separator,
    the code either outputs a fix sequence or "FAILED".

    try_horizontal_separator: whether we use horizontal separators or only the vertical (main) one
    sub_separator parameters correspond to an additional feature we ended up
    not needing in our results.
    """

    #all_patterns = list(permutations(range(1, 1+pattern_length)))
    pattern_groups = symmetry_groups(pattern_length)
    group_representatives = [g[0] for g in pattern_groups] 
    if output_path is not None:
        f = open(output_path, "w")
        f.write("Number of symmetry groups (up to horizontal or vertical reflection): %d\n" \
                % (len(group_representatives),))
        f.write("Use horizontal separator? " + str(try_horizontal_separator) + "\n")
        f.write("Use vertical sub-separator? " +str(try_sub_separator) + "\n")
        f.write("Use horizontal sub-separator? " + str(try_horizontal_sub_separator) + "\n")
        f.close()
    for pattern in group_representatives:
        for main_separator in range(1, len(pattern)):
            if try_horizontal_separator:
                for horizontal_separator in range(2, len(pattern)+1):
                    outcome, p_list = run(pattern, 
                        main_separator=main_separator, 
                        horizontal_separator=horizontal_separator, 
                        try_sub_separator=try_sub_separator, 
                        try_horizontal_sub_separator=try_horizontal_sub_separator, 
                        debug_print=debug_print)
                    for p in p_list:
                        output_string = p.initial_state_string + " ---> " + ", ".join(p.fix_sequence)
                        print(output_string)
                        if output_path is not None:
                            f = open(output_path, "a")
                            f.write(output_string + "\n")
                            f.close()
            else:
                outcome, p_list = run(pattern, 
                    main_separator=main_separator, 
                    horizontal_separator=None, 
                    try_sub_separator=try_sub_separator, 
                    try_horizontal_sub_separator=False, 
                    debug_print=debug_print)
                for p in p_list:
                    output_string = p.initial_state_string + " ---> " + ", ".join(p.fix_sequence)
                    print(output_string)
                    if output_path is not None:
                        f = open(output_path, "a")
                        f.write(output_string + "\n")
                        f.close()   
            
                
run_main_code(6, 
              try_horizontal_separator=True, 
              try_sub_separator=True, 
              try_horizontal_sub_separator=True, 
              debug_print=False, 
              output_path="6-patterns-with-sub-separators.txt")
