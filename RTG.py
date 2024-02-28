import pyparsing as pp
from pyparsing import pyparsing_common as ppc
import numpy as np
import sys

class Random_Table_Generator:
    
    def __init__(
        self,
        distribution_modifier=1,
        tables_folder = 'tables',
        input_phrase = None,
        default_chance_increase = 2,
        default_chance_decrease = 0.5,
        default_option = 0.5,
        default_boolean = 0.5,
        loop_limit = 100,
        dist_dict = {
            'vlo': 0.9,
            'lo':  0.7,
            'med': 0.3,
            'hi':  0.2,
            'vhi': 0.1
        }
    ):
        self.distribution = distribution_modifier
        self.default_chance_increase = default_chance_increase
        self.default_chance_decrease = default_chance_decrease
        self.default_option = default_option
        self.default_boolean = default_boolean
        self.tables_folder = tables_folder
        self.input_phrase = input_phrase
        self.loop_limit = loop_limit
        self.loops = 0
        self.dist_dict = dist_dict

        # defining patterns for pyparsing
        self.option_pat_combo    = '%' + pp.Opt(ppc.fnumber()) + pp.nested_expr(opener='[', closer=']')
        self.option_pat_combo2   = pp.original_text_for('%' + pp.Opt(ppc.fnumber()('chance')) + '.' + pp.original_text_for(pp.nested_expr(opener='[', closer=']'))('heads') + pp.Opt('.') + pp.original_text_for(pp.Opt((pp.nested_expr(opener='[', closer=']'))))('tails'))
        self.option_pat_indiv_orig    = '%' + pp.Opt(ppc.fnumber()('chance')) + '.' + pp.original_text_for(pp.nested_expr(opener='[', closer=']'))('heads') + pp.Opt('.') + pp.original_text_for(pp.Opt(pp.nested_expr(opener='[', closer=']')))('tails')
        self.option_pat_indiv    = '%' + pp.Opt(ppc.fnumber()('chance')) + '.' + pp.original_text_for(pp.nested_expr(opener='[', closer=']'))('heads') + pp.Opt('.') + pp.original_text_for(pp.Opt(pp.nested_expr(opener='[', closer=']')))('tails') 
        self.table_pat           = pp.Combine('@' + pp.Word(pp.printables, exclude_chars=']'))
        self.number_pat_combo    = pp.Combine('#' + pp.Word(pp.printables))
        self.number_pat_indiv    = '#' + pp.Word(pp.alphas)('dist') + pp.Opt('.') + pp.Opt(pp.Word(pp.nums)('max'))
        self.boolean_pat_combo   = pp.Combine('$' + pp.Opt(ppc.fnumber) + "." + pp.Word(pp.alphanums) + "." + pp.Word(pp.alphanums))
        self.boolean_pat_indiv   = '$' + pp.Opt(ppc.fnumber)('chance') + "." + pp.Word(pp.alphanums)('heads') + "." + pp.Word(pp.alphanums)('tails')
        self.chance_increase_pat = pp.Combine(pp.StringStart() + '^' + pp.Opt(ppc.fnumber()))
        self.chance_decrease_pat = pp.Combine(pp.StringStart() + '*' + pp.Opt(ppc.fnumber()))
        
        
    def process_input_file(self, input_file):
        file = open(input_file, 'r').read().split('\n')
        for line in file:
            processed_line = self.process_input_line(line)
            print(processed_line)
            
            
    def process_input_phrase(self, input_phrase):
        processed_line = self.process_input_line(input_phrase)
        print(processed_line)
    
    
    def test_process_input_line(self, line):
        # this is for testing the compact dictionary version of process_input_line.
        pass
    
    
    def process_input_line(self, line):
        # the expanded version that works without the pat_dict
        # print('PROCESS LINE INPUT: ', line)
        gen_check = False
        outputs = []
        matches_option_pat = self.option_pat_combo2.scan_string(line)
        for match, start, stop in matches_option_pat:
            gen_check = True
            output = self.process_input_line(self.process_option(match))
            outputs.append((match, output, start, stop))
        if gen_check:
            line = self.replace(line, outputs)
        
        gen_check = False
        outputs = []
        matches_table_pat = self.table_pat.scan_string(line)
        for match, start, stop in matches_table_pat:
            gen_check = True
            output = self.process_input_line(self.process_table(match))
            outputs.append((match, output, start, stop))
        if gen_check:
            line = self.replace(line, outputs)
        
        gen_check = False
        outputs = []
        matches_number_pat = self.number_pat_combo.scan_string(line)
        for match, start, stop in matches_number_pat:
            gen_check = True
            output = self.process_input_line(self.process_number(match))
            outputs.append((match, output, start, stop))
        if gen_check:
            line = self.replace(line, outputs)
        
        gen_check = False
        outputs = []
        matches_boolean_pat = self.boolean_pat_combo.scan_string(line)
        for match, start, stop in matches_boolean_pat:
            gen_check = True
            output = self.process_input_line(self.process_boolean(match))
            outputs.append((match, output, start, stop))
        if gen_check:
            line = self.replace(line, outputs)
        # print('PROCESS LINE OUTPUT: ',line)
        return line

    
    def replace(self, line, mappings):
        # print('REPLACE INPUTS:')
        # print('\t', line)
        # print('\t', mappings)
        slices, indices, output = [], [0], []
        for mapping,_, start, end in mappings:
            if str(mapping[0])[-1] == ' ':
                end -= 1
            indices += [start,end]

        # if len(line) != mappings[-1][-1]:
        #     indices += [None]
        indices += [None]
        # print('INDICES: ', indices)
        for i in range(0,len(indices),2):
            slices.append(slice(indices[i], indices[i+1]))
        # print('SLICES: ', slices)
        if mappings[0][2] == 0:
            # print('WHERE I THINK THE ISSUE IS')
            for new_word, i in zip([i[1] for i in mappings], slices):
                # print('NEW WORD: ',new_word)
                # print('NEXT LINE PART: ', line[i])
                output += [new_word, line[i]]
            output += [line[slices[-1]]] 
        else:
            for new_word, i in zip([i[1] for i in mappings], slices):
                output += [line[i], new_word]
            if len(mappings) < len(slices):
                output += [line[slices[-1]]] 
        output = [str(i) for i in output]
        # print('REPLACE OUTPUTS: ', output)
        return ''.join(output)

    
    def process_option(self, instruction):
        for match, start, stop in self.option_pat_indiv.scan_string(instruction):
            if match.chance == '':
                probability = self.default_boolean
            else:
                probability = match.chance
            random_value = np.random.random()
            
            return (match.heads[1:-1] if random_value <= probability else match.tails[1:-1])
    
    
    def process_table(self, reference):
        input_file = self.tables_folder + '/' + reference[0][1:] + '.txt'
        file = open(input_file, 'r').read().split('\n')

        probabilities = np.ones(len(file))

        for line_no, line in enumerate(file):
            matches_increase = self.chance_increase_pat.scan_string(line)
            for match, start, end in matches_increase:
                if end == 1:
                    probabilities[line_no] = self.default_chance_increase
                else:
                    probabilities[line_no] = float(match[0][1:])
                file[line_no] = line[(end+1):]

            matches_decrease = self.chance_decrease_pat.scan_string(line)
            for match, start, end in matches_decrease:
                if end == 1:
                    probabilities[line_no] = self.default_chance_decrease
                else:
                    probabilities[line_no] = float(match[0][1:])
                file[line_no] = line[(end+1):]

        probabilities_cum = np.cumsum(probabilities)
        random_value = np.random.uniform(0,probabilities.sum(),1)
        pick = np.argmax((probabilities_cum // random_value)>0)
        
        return file[pick]
    
    
    def process_number(self, instruction):
        for match, start, end in self.number_pat_indiv.scan_string(instruction):
            random_value = np.random.geometric(p=self.dist_dict[match.dist])
            if match.max == '':
                return random_value
            else:
                return (str(random_value) if int(match.max) > random_value else match.max)
    
    
    def process_boolean(self, instruction):
        for match, start, end in self.boolean_pat_indiv.scan_string(instruction):
            if match.chance == '':
                probability = self.default_boolean
            else:
                probability = match.chance
            random_value = np.random.random()
            return (match.heads if random_value <= probability else match.tails)
    
    
            
if __name__ == "__main__":
    rtg = Random_Table_Generator()
    if sys.argv[1][-4:] == '.txt':
        rtg.process_input_file(sys.argv[1])
    else:
        rtg.process_input_phrase(sys.argv[1])