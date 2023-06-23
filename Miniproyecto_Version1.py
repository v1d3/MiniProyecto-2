#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class QuadTree:
    def __init__(self, boundary, max_points=4, depth=0):
        self.boundary = boundary
        self.max_points = max_points
        self.points = []
        self.depth = depth
        self.divided = False

    def totalPoints(self):
        count = len(self.points)
        if self.divided:
            count += self.nw.totalPoints() + self.ne.totalPoints() + self.se.totalPoints() + self.sw.totalPoints()
        return count

    def totalNodes(self):
        count = 1  # Cuenta el nodo actual
        if self.divided:
            count += self.nw.totalNodes() + self.ne.totalNodes() + self.se.totalNodes() + self.sw.totalNodes()
        return count

    def insert(self, point, data):
        if not self.boundary.contains(point):
            return False
        if len(self.points) < self.max_points:
            self.points.append((point, data))
            return True
        if not self.divided:
            self.divide()
        return (self.ne.insert(point, data) or
                self.nw.insert(point, data) or
                self.se.insert(point, data) or
                self.sw.insert(point, data))

    def list(self):
        point_list = []
        for point, data in self.points:
            point_list.append((point.x, point.y, data))
        if self.divided:
            point_list.extend(self.nw.list())
            point_list.extend(self.ne.list())
            point_list.extend(self.se.list())
            point_list.extend(self.sw.list())
        return point_list

    def countRegion(self, point, d):
        count = 0
        if self.boundary.contains_point((point.x, point.y)) and self.boundary.contains_point((point.x + d, point.y + d)):
            for p, _ in self.points:
                if self.boundary.contains_point((p.x, p.y)) and self.distance_to(p, point) <= d:
                    count += 1
            if self.divided:
                count += self.nw.countRegion(point, d)
                count += self.ne.countRegion(point, d)
                count += self.se.countRegion(point, d)
                count += self.sw.countRegion(point, d)
        return count

    def aggregateRegion(self, point, d):
        population = 0
        if self.boundary.contains_point((point.x, point.y)) and self.boundary.contains_point((point.x + d, point.y + d)):
            for p, data in self.points:
                if self.boundary.contains_point((p.x, p.y)) and self.distance_to(p, point) <= d:
                    population += data
            if self.divided:
                population += self.nw.aggregateRegion(point, d)
                population += self.ne.aggregateRegion(point, d)
                population += self.se.aggregateRegion(point, d)
                population += self.sw.aggregateRegion(point, d)
        return population

    def divide(self):
        # Implementa la división del QuadTree en cuatro subcuadrantes
        x = self.boundary.get_x()
        y = self.boundary.get_y()
        w = self.boundary.get_width() / 2
        h = self.boundary.get_height() / 2

        nw_boundary = Rectangle((x, y + h), w, h)
        ne_boundary = Rectangle((x + w, y + h), w, h)
        sw_boundary = Rectangle((x, y), w, h)
        se_boundary = Rectangle((x + w, y), w, h)

        self.nw = QuadTree(nw_boundary, self.max_points, self.depth + 1)
        self.ne = QuadTree(ne_boundary, self.max_points, self.depth + 1)
        self.sw = QuadTree(sw_boundary, self.max_points, self.depth + 1)
        self.se = QuadTree(se_boundary, self.max_points, self.depth + 1)

        self.divided = True

    def distance_to(self, p1, p2):
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


# Crear un QuadTree con una región rectangular de prueba
boundary = Rectangle((0, 0), 10, 10)
quadtree = QuadTree(boundary, max_points=4)

# Insertar algunos puntos de prueba en el QuadTree
point1 = Point(2, 3)
point2 = Point(5, 7)
point3 = Point(8, 4)
point4 = Point(6, 2)
quadtree.insert(point1, 100)
quadtree.insert(point2, 200)
quadtree.insert(point3, 300)
quadtree.insert(point4, 400)

# Obtener la cantidad de puntos almacenados en el QuadTree
total_points = quadtree.totalPoints()
print("Total Points:", total_points)  # Salida: 4

# Obtener la cantidad de nodos en el QuadTree
total_nodes = quadtree.totalNodes()
print("Total Nodes:", total_nodes)  # Salida: 9

# Obtener una lista de todos los puntos almacenados en el QuadTree
point_list = quadtree.list()
print("Point List:")
for point in point_list:
    print(point)
# Salida:
# (2.0, 3.0, 100)
# (5.0, 7.0, 200)
# (8.0, 4.0, 300)
# (6.0, 2.0, 400)

# Contar la cantidad de puntos dentro de una región circular
center_point = Point(5, 5)
radius = 4
count = quadtree.countRegion(center_point, radius)
print("Points in Region:", count)  # Salida: 3

# Calcular la suma de la población dentro de una región 
population = quadtree.aggregateRegion(center_point, radius)
print("Population in Region:", population)  # Salida: 1000


# In[ ]:




