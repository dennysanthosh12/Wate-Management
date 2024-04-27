
import numpy as np
from math import radians, sin, cos, sqrt, asin


class TSPBranchBound:
    def __init__(self, graph):
        self.graph = graph
        self.num_cities = len(graph)
        self.visited = [False] * self.num_cities
        self.best_path = None
        self.best_cost = np.inf

    def bound(self, path):
        cost = 0
        unvisited = [i for i in range(self.num_cities) if not self.visited[i]]
        for i in range(len(path) - 1):
            cost += self.graph[path[i]][path[i + 1]]
        if len(path) == self.num_cities:
            cost += self.graph[path[-1]][path[0]]
        else:
            min_outgoing = min(self.graph[path[-1]][j] for j in unvisited)
            min_incoming = min(self.graph[i][path[0]] for i in unvisited)
            cost += min_outgoing + min_incoming
        return cost

    def branch_and_bound(self, path, cost):
        if len(path) == self.num_cities:
            # Add the cost to return to the starting node
            cost += self.graph[path[-1]][path[0]]
            if cost < self.best_cost:
                # Update best path and cost
                self.best_cost = cost
                self.best_path = path + [path[0]]  # Ensure path returns to start
            return
        
        if cost >= self.best_cost:
            return
        
        for i in range(self.num_cities):
            if not self.visited[i]:
                self.visited[i] = True
                self.branch_and_bound(path + [i], cost + self.graph[path[-1]][i])
                self.visited[i] = False

    def solve(self, start_node=0):
        self.visited[start_node] = True
        self.branch_and_bound([start_node], 0)
        return self.best_path, self.best_cost

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    
    # Calculate the distance
    distance = R * c
    return distance

