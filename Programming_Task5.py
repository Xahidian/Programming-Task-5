import csv
from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]
        self.edge_ids = {}
        self.matching = [-1] * vertices
        self.parent = [-1] * vertices
        self.base = list(range(vertices))
        self.blooming = [False] * vertices
        self.used = [False] * vertices

    def add_edge(self, u, v, edge_id):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.edge_ids[(u, v)] = edge_id
        self.edge_ids[(v, u)] = edge_id

    def find_root(self, u):
        while u != self.base[u]:
            u = self.base[u]
        return u

    def mark_path(self, u, v, b):
        while self.find_root(u) != b:
            self.blooming[self.base[u]] = self.blooming[self.base[self.matching[u]]] = True
            self.parent[u] = v
            v = self.matching[u]
            u = self.parent[u]

    def find_blossom(self, u, v):
        root = self.find_root(u)
        while True:
            self.blooming[root] = True
            if self.matching[root] == -1:
                break
            root = self.find_root(self.parent[self.matching[root]])
        root = self.find_root(v)
        while not self.blooming[root]:
            root = self.find_root(self.parent[self.matching[root]])
        return root

    def blossom_contract(self, u, v, blossom_base):
        for i in range(self.V):
            self.blooming[i] = False
        self.mark_path(u, v, blossom_base)
        self.mark_path(v, u, blossom_base)
        if self.find_root(u) != blossom_base:
            self.parent[u] = v
        if self.find_root(v) != blossom_base:
            self.parent[v] = u
        for i in range(self.V):
            if self.blooming[self.find_root(i)]:
                self.base[i] = blossom_base
                if not self.used[i]:
                    self.used[i] = True
                    self.queue.append(i)

    def find_augmenting_path(self, start):
        self.queue = deque([start])
        self.parent = [-1] * self.V
        self.used = [False] * self.V
        self.base = list(range(self.V))
        self.used[start] = True
        while self.queue:
            u = self.queue.popleft()
            for v in self.graph[u]:
                if self.find_root(u) == self.find_root(v):
                    continue
                if v == start or (self.matching[v] != -1 and self.parent[self.matching[v]] != -1):
                    blossom_base = self.find_blossom(u, v)
                    self.blossom_contract(u, v, blossom_base)
                elif self.parent[v] == -1:
                    self.parent[v] = u
                    if self.matching[v] == -1:
                        self.augment_matching(v)
                        return True
                    self.queue.append(self.matching[v])
                    self.used[self.matching[v]] = True
        return False

    def augment_matching(self, v):
        while v != -1:
            u = self.parent[v]
            next_v = self.matching[u]
            self.matching[u] = v
            self.matching[v] = u
            v = next_v

    def find_maximum_matching(self):
        for u in range(self.V):
            if self.matching[u] == -1:
                self.find_augmenting_path(u)
        return self.matching

def read_csv_and_create_graph(csv_filename):
    with open(csv_filename, newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header row
        edges = list(reader)
    vertex_set = set()
    for edge in edges:
        u, v, _ = edge
        u, v = int(u[1:]), int(v[1:])
        vertex_set.update([u, v])
    graph = Graph(max(vertex_set))  # Graph vertices count
    for edge in edges:
        u, v, edge_id = edge
        u, v = int(u[1:]), int(v[1:])
        graph.add_edge(u-1, v-1, edge_id)  # Adjust for 0-indexed vertices
    return graph

# Example usage:
graph = read_csv_and_create_graph('benchmark4.csv')
matching = graph.find_maximum_matching()

# Extracting and writing the matched edge IDs to a TXT file
matched_edge_ids = []
for i in range(len(matching)):
    if matching[i] != -1 and i < matching[i]:
        edge_id = graph.edge_ids.get((i, matching[i]))
        if edge_id:
            matched_edge_ids.append(edge_id)

# Print the maximum cardinality matching
print("Maximum cardinality matching is:", ','.join(matched_edge_ids))

# Write the matched edge IDs to a TXT file
with open('Blossom_max_card_matching.txt', 'w') as f:
    f.write(','.join(matched_edge_ids))
