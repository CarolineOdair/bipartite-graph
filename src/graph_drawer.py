import numpy as np
import matplotlib.pyplot as plt

class GraphDrawer():
    def __init__(self, graph):
        self.GRAPH = graph
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot()

    def draw(self) -> plt:
        n = self.GRAPH.NUMBER_OF_VERTICES

        points = [i for i in range(n)]

        self.ax.scatter(x = [0 for i in range(n)], y = points, color = "blue", s = 50)
        self.ax.scatter(x = [n-1 for i in range(n)], y = points, color = "green", s = 50)

        self.fig.grid()

        return self.fig