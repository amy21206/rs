import difflib
import pandas as pd
from collections import namedtuple
from .get_parsons_code_distractors import *
from .generate_parsons_blocks import *
# import textwrap
# import json
# compare the similarity between the student code and the fixed code

#  It prints the difference between the two code snippets line by line using a loop. It also prints the similarity ratio.

# Please note that the difflib module compares lines based on their content, 
# so it may not capture more complex differences, such as code structure or logic.

CodeComparison = namedtuple('CodeComparison', ['student_removed', 'fixed_modified', 'line_similarity'])

def compare_code(buggy_code, fixed_code):
    #print(fixed_code)
    code_comparison_pairs = []
    # Split the code into lines
    student_lines = buggy_code.splitlines(keepends=True)
    fixed_lines = fixed_code.splitlines(keepends=True)

    # Perform a line-based comparison
    diff = list(difflib.Differ().compare(student_lines, fixed_lines))

    # Calculate similarity ratio
    total_similarity = difflib.SequenceMatcher(None, buggy_code, fixed_code).ratio()

    #print("diff here\n", diff)
    # Get the line similarity pairs
    line_similarity_pairs = []
    fixed_lines = []
    removed_lines = []
    unchanged_lines = []
    discarded_lines = []
    for i, line in enumerate(diff):
        if line.startswith('+'):
            fixed_lines.append((i, len(line[1:].strip()), line[2:]))
        elif line.startswith('-'):
            removed_lines.append((i, len(line[1:].strip()), line[2:]))
        elif line.startswith('?'):
            discarded_lines.append((i, len(line[1:].strip()), line[2:]))
        else:
            unchanged_lines.append((i, len(line[1:].strip()), line[2:]))
    #print("compare_code", fixed_lines, removed_lines, unchanged_lines)
    # Pair up the added and removed lines
    max_len = max(len(fixed_lines), len(removed_lines))

    for i in range(max_len):
        try:
            line_similarity_pairs.append((['student', removed_lines[i]], ['fixed', fixed_lines[i]]))
        except IndexError:
            if len(fixed_lines) > len(removed_lines):
                line_similarity_pairs.append((['student', (0, '', '')], ['fixed', fixed_lines[i]]))
            else:
                line_similarity_pairs.append((['student', removed_lines[i]], ['fixed', (0, '', '')]))
            
    # one line similarity > 30%
    #Calculate similarity ratio only for different lines
    for i, pair in enumerate(line_similarity_pairs):
        if pair[0][1] != pair[1][1]:
            similarity = difflib.SequenceMatcher(None, pair[0][1][2], pair[1][1][2]).ratio()
            pair = CodeComparison(pair[0][1], pair[1][1], similarity)
            code_comparison_pairs.append(pair)
     
    return code_comparison_pairs, fixed_lines, unchanged_lines, total_similarity

# Decide which type of Parsons problem we will generate and generate the corresponding distractors
def personalize_Parsons_block(df_question_line, code_comparison_pairs, fixed_lines, unchanged_lines, total_similarity):
    distractors = {}
    #print("code_comparison_pairs\n", code_comparison_pairs, "total_similarity\n", total_similarity)
    if total_similarity < 0.3:
        return "Full", distractors
    # have more than 3 wrong lines
    elif (total_similarity >= 0.3)&(len(code_comparison_pairs)>=3):
        # check each line_similarity
        for pair in code_comparison_pairs:
            if pair[2] > 0.20:
                #print("pair to generate distractors", pair)
                # ask OpenAI to generate a distractor
                #print("the correct line that had bugs before\n", pair[1][2])
                distractor = get_personalized_distractor(build_distractor_prompt(df_question_line, pair[1][2]),pair[1][2])
                distractors[pair[1]] =  distractor
            else:
                continue
        return "Partial", distractors
    elif (total_similarity >= 0.3)&(len(code_comparison_pairs)<3):
        # first check if there is any line_similarity > 0.3 - distractor contributed by students
        for pair in code_comparison_pairs:
            if pair[2] > 0.20:
                # ask OpenAI to generate a distractor
                distractor = get_personalized_distractor(build_distractor_prompt(df_question_line, pair[1][2]),pair[1][2])
                distractors[pair[1]] =  distractor
            else:
                continue
        # if no line_similarity > 0.3, generate the distractor from the top 3 longest lines
        if len(distractors) == 0:
            distractor_candidates = sorted(fixed_lines + unchanged_lines, key=lambda x: x[1], reverse=True)[:3]
            for distractor_candidate in distractor_candidates:
                distractor = get_personalized_distractor(build_distractor_prompt(df_question_line, distractor_candidate[2]))
                # the keys should be tuple (location, length, code) instead of only the actual code
                distractors[distractor_candidate] = distractor
        return "Partial_random", distractors
