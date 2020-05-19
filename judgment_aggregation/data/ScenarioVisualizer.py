import pandas as pd
import numpy as np


class ScenarioVisualizer:
    """A class used to visualize loaded Scenarios"""
    def __init__(self, scenario, solutions=None, show_majority=False):
        if not scenario.get_judgments:
            raise ValueError("ScenarioVisualizer scenario argument should be"
                             " a Scenario instance.")
        individual, judges_per_judgment = scenario.get_judgments()
        self.data = individual.copy()
        self.index = judges_per_judgment.copy()
        self.index = [str(i) + " judge(s)" for i in self.index]
        collective = scenario.get_collective_judgments()
        if solutions is not None:
            collective += solutions
        self.data += list(map(lambda x: list(map(bool, x)), collective))
        self.index += [
            "Collective Judgment " + str(i + 1) for i in range(len(collective))
        ]

        if show_majority:
            self.data += [
                list(
                    np.array(individual).T @ judges_per_judgment >= .5 *
                    np.sum(judges_per_judgment))
            ]
            self.index += ["Majority"]

        self.columns = scenario.get_issue_names()

    def get_dataframe(self):
        return pd.DataFrame(self.data, self.index, self.columns, dtype=bool)\

    def plot_data(self, ax):
        """Plot the the data in a matplotlib table; give a matplotlib axis
        as argument and the table is plotted there."""
        data = [[c] + d for c, d in zip(self.index, self.data)]
        colors = np.empty_like(data)
        for i in range(len(data)):
            for j in range(len(data[0])):
                if j == 0:
                    colors[i, j] = 'w'
                elif data[i][j]:
                    colors[i, j] = 'g'
                else:
                    colors[i, j] = 'r'
        the_table = ax.table(cellText=data,
                             colLabels=['judge(s)'] + self.columns,
                             cellColours=colors,
                             loc='center',
                             cellLoc='center')
        the_table.auto_set_font_size()
        the_table.auto_set_column_width(list(range(len(data))))
        ax.axis('off')
