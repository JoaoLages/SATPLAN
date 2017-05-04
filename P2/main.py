import argparse
import itertools
from utils import *
from action import Action
from sat_plan import *
from copy import deepcopy
import time
import sys


def get_input():
    parser = argparse.ArgumentParser(description='Input information.')
    parser.add_argument("filename")

    return parser.parse_args()


def get_predicates(line, predicates):

    for word in line:
        if word[0] == '-':
            continue
        else:
            pred = word[0: word.find("(")]
            args_str = word[word.find("(") + 1:word.find(")")]
            args = args_str.split(',')
            predicates.add((pred, len(args)))
    return predicates


def get_constants(line, constants):

    for word in line:
        new_word = word[word.find("(") + 1:word.find(")")]
        consts = new_word.split(',')
        constants.update(consts)

    return constants


def get_action(line):
    action_name = line[1]

    precond_pos, precond_neg, effect_pos, effect_neg = [], [], [], []
    i = 0
    for i, word in enumerate(line[3:]):
        if word != "->":
            if word[0] != '-':
                precond_pos.append(to_atom(word))
            else:
                precond_neg.append(to_atom(word[1:]))
        else:
            break
    for word in line[3 + (i + 1):]:
        if word[0] != '-':
            effect_pos.append(to_atom(word))
        else:
            effect_neg.append(to_atom(word[1:]))

    return Action(to_atom(action_name), [precond_pos, precond_neg], [effect_pos, effect_neg])


def get_state(line):
    state = []
    for atom in line:
        state.append(to_atom(atom))

    return state


def process_file(file):
    initial_state, actions, goal_state = [], [], []
    constants = set()
    predicates = set()
    # process input file
    for i, line in enumerate(file):

        words = line.split()
        if len(words) > 0:

            # initial state line
            if words[0] == 'I':
                # extract constants
                constants = get_constants(words[1:], constants)
                predicates = get_predicates(words[1:], predicates)
                initial_state = get_state(words[1:])


            # action line
            elif words[0] == 'A':
                actions.append(get_action(words))
                predicates = get_predicates(words[3:], predicates)

            # goal state line
            elif words[0] == 'G':
                goal_state = get_state(words[1:])
                constants = get_constants(words[1:], constants)
                predicates = get_predicates(words[1:], predicates)
            else:
                error_msg = "1st character of line " + str(i) + " does not follow specified format"
                raise ValueError(error_msg)

    return initial_state, constants, actions, goal_state, predicates


def generate_action_comb(action_list, constants):
    combinations = {}
    for action in action_list:
        combinations[action.name] = list(itertools.product(constants, repeat=len(action.args)))

    return combinations


def generate_predicate_comb(predicates, constants):
    combinations = {}
    for pred in predicates:
        combinations[pred[0]] = list(itertools.product(constants, repeat=pred[1]))
    return combinations


def ground_predicates(dict):
    """
    Receives a dictionary with the name of the predicate and all combinations to ground it
    """
    atoms = []
    for pred in dict:
        for comb in dict[pred]:
            expr = []
            for c in comb:
                expr.append(Atom(c))
            atoms.append(Atom(pred, *expr))
    return atoms


def ground_actions(dict, actions):
    atoms = []
    for i, pred in enumerate(dict):
        for comb in dict[pred]:
            for action in actions:
                if action.name == pred:
                    break
            precond_n, precond_p, effect_add, effect_rem = action.substitute(list(comb))
            if not any([i in effect_add for i in effect_rem]):
                expr = []
                for c in comb:
                    expr.append(Atom(c))
                atoms.append(Atom(pred, *expr))
    return atoms


def main():
    input_args = get_input()

    file = open(input_args.filename, "r")

    initial_state, constants, actions, goal_state, predicates = process_file(file)

    pred_comb = generate_predicate_comb(predicates, constants)
    grounded_predicates = ground_predicates(pred_comb)

    action_comb = generate_action_comb(actions, constants)
    grounded_actions = ground_actions(action_comb, actions)
    solution = SAT_plan(tuple(initial_state), constants, actions, grounded_predicates, grounded_actions, tuple(goal_state), sys.maxsize)
    # print solution to terminal
    for action in solution:
        print(action)

if __name__ == '__main__':
    main()
