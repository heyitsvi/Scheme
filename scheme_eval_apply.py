import sys
import os

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    # print("DEBUG: first ", first)
    # print("DEBUG: rest ", rest)
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        # print("DEBUG: is true",isinstance(scheme_eval(first, env), Procedure))
        operator_eval = scheme_eval(first, env)
        if isinstance(operator_eval, Procedure):
             mapped_list = rest.map(lambda x: scheme_eval(x, env))
            #  print("DEBUG : mapped list ", mapped_list)
             return scheme_apply(operator_eval, mapped_list,env)
        else:
            raise SchemeError("Unknown operator type")
        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        lst_of_args = []

        while(args is not nil):
            lst_of_args.append(args.first)
            args = args.rest

        # print("DEBUG:", lst_of_args)

        if procedure.expect_env:
            lst_of_args.append(env)

        try:
            return procedure.py_func(*lst_of_args)
        except TypeError as e:
            raise SchemeError('incorrect number of arguments')
        # END PROBLEM 2
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        # print("DEBUG: Args First ", args.first)
        # print("DEBUG: Args Rest ", args.rest)
        # print("DEBUG Formal Args ",procedure.formals)
        new_frame = procedure.env.make_child_frame(procedure.formals, args)
        # print("DEBUG: --->", new_frame)
        return eval_all(procedure.body, new_frame)
        
        
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        # print("DEBUG: Procedure Body ",procedure.body)
        new_frame = env.make_child_frame(procedure.formals,args)
        return eval_all(procedure.body, new_frame)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    if expressions is not nil:
        while(expressions is not nil):
            if expressions.rest is nil:
                return scheme_eval(expressions.first, env)
            else:
                scheme_eval(expressions.first, env)
                expressions = expressions.rest

      # replace this with lines of your own code
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(original_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
# scheme_eval = optimize_tail_calls(scheme_eval)
