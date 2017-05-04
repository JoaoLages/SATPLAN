from copy import deepcopy


class Action:
    """ Given an Atom(action) and its preconditions and effects creates an Action"""
    def __init__(self, action, precond, effect):
        self.name = action.operator
        self.args = action.args
        self.precond_pos = precond[0]
        self.precond_neg = precond[1]
        self.effect_add = effect[0]
        self.effect_rem = effect[1]

    def substitute(self, args): # receives args (A,B) and returns name, preconds and effects
        precond_sub_pos = deepcopy(self.precond_pos)
        precond_sub_neg = deepcopy(self.precond_neg)
        effect_sub_add = deepcopy(self.effect_add)
        effect_sub_rem = deepcopy(self.effect_rem)

        for i, arg in enumerate(self.args): # arg = b
            variable = deepcopy(arg)

            for j, atom in enumerate(precond_sub_neg):  # atom= On(b,f)
                precond_sub_neg[j].args = list(precond_sub_neg[j].args)
                for k, arg_atom in enumerate(atom.args):  # arg_atom = b
                    if arg_atom == variable:
                        precond_sub_neg[j].args[k] = args[i]

            for j, atom in enumerate(precond_sub_pos):  # atom= On(b,f)
                precond_sub_pos[j].args = list(precond_sub_pos[j].args)
                for k, arg_atom in enumerate(atom.args):  # arg_atom = b
                    if arg_atom == variable:
                        precond_sub_pos[j].args[k] = args[i]

            for j, atom in enumerate(effect_sub_add):  # atom= On(b,f)
                effect_sub_add[j].args = list(effect_sub_add[j].args)
                for k, arg_atom in enumerate(atom.args):  # arg_atom = b
                    if arg_atom == variable:
                        effect_sub_add[j].args[k] = args[i]

            for j, atom in enumerate(effect_sub_rem):  # atom= On(b,f)
                effect_sub_rem[j].args = list(effect_sub_rem[j].args)
                for k, arg_atom in enumerate(atom.args):  # arg_atom = b
                    if arg_atom == variable:
                        effect_sub_rem[j].args[k] = args[i]

        return precond_sub_neg, precond_sub_pos, effect_sub_add, effect_sub_rem
