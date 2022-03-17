"""
@author: Ethan Gu
@file: evo.py: An evolutionary computing framework (version 4)
Assumes no Solutions class.
"""

import random as rnd
import copy
from functools import reduce
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def final_results_as_csv(solutions):
    """Takes the final results and returns a csv file"""
    summary_table = pd.DataFrame()
    solutions = list(solutions)
    sol_df = pd.DataFrame(columns=['teamname', 'setups', 'lowpriority', 'delays'])
    helper_dict = dict()
    for i in solutions:
        helper_dict['setups'] = i[0][1]
        helper_dict['lowpriority'] = i[1][1]
        helper_dict['delays'] = i[2][1]

        helper_dict['teamname'] = 'Ethan Gu'
        sol_df = sol_df.append(helper_dict, ignore_index=True)
    sol_df.to_csv(r'C:\Users\ethan\Desktop\summary_table.csv', sep=',')
    #print(sol_df)
    plot = sns.pairplot(sol_df)
    plt.show()




class Evo:

    def __init__(self):
        """ Population constructor """
        self.pop = {}  # The solution population eval -> solution
        self.fitness = {}  # Registered fitness functions: name -> objective function
        self.agents = {}  # Registered agents:  name -> (operator, num_solutions_input)
        self.evals = {}

    def size(self):
        """ The size of the current population """
        return len(self.pop)

    def add_fitness_criteria(self, name, f):
        """ Register a fitness criterion (objective) with the
        environment. Any solution added to the environment is scored
        according to this objective """
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ Register a named agent with the population.
        The operator (op) function defines what the agent does.
        k defines the number of solutions the agent operates on. """
        self.agents[name] = (op, k)

    def add_solution(self, sol):
        """ Add a solution to the population """
        # eval = ((obj1, score1), (obj2, score2).....)
        eval = tuple((name, f(sol)) for name, f in self.fitness.items())
        self.pop[eval] = sol

    def add_eval(self, iteration, evals):
        """Add a fitness objective to a separate dictionary for graphing purposes"""
        self.evals[iteration] = evals

    def run_agent(self, name):
        """ Invoke an agent against the population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    def evolve(self, n=1, dom=100, status=100):
        """ Run n random agents (default=1)
        dom defines how often we remove dominated (unfit) solutions
        status defines how often we display the current population """

        agent_names = list(self.agents.keys())
        for i in range(n):
            pick = rnd.choice(agent_names)
            self.run_agent(pick)

            if i % dom == 0:
                self.remove_dominated()

            if i % status == 0:
                self.remove_dominated()
                self.add_eval(i, list(self.pop.keys()))
                print("Iteration:", i)
                print("Population size:", self.size())
                print(self.pop.keys())

        # Clean up the population
        self.remove_dominated()
        final_results_as_csv(self.pop.keys())


    def get_random_solutions(self, k=1):
        """ Pick k random solutions from the population """
        if self.size() == 0:
            return []
        else:
            solutions = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(solutions)) for _ in range(k)]

    @staticmethod
    def _dominates(p, q):
        """ p = evaluation of solution: ((obj1, score1), (obj2, score2), ... )"""
        pscores = [score for _, score in p]
        qscores = [score for _, score in q]
        score_diffs = list(map(lambda x, y: y - x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p, q)}

    def remove_dominated(self):
        """ Remove dominated solutions """
        nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    def show_evals(self):
        return self.evals

    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval, sol in self.pop.items():
            rslt += str(dict(eval)) + ":\t" + str(sol) + "\n"
        return rslt