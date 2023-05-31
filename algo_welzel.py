import math
import os
import random

# Structure de données pour un point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Structure de données pour un cercle
class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

# Algorithme Welzl pour le cercle minimum englobant
def welzl(points):
    def welzl_recursive(points, boundary):
        if len(points) == 0 or len(boundary) == 3:
            return minidisk(boundary)
        
        # Sélectionner un point aléatoire
        p = random.choice(points)
        
        # Récursion sans le point sélectionné
        circle = welzl_recursive([q for q in points if q != p], boundary)
        if circle_contains(circle, p):
            return circle
        
        # Récursion avec le point sélectionné
        return welzl_recursive([q for q in points if q != p], boundary + [p])
    
    return welzl_recursive(points, [])

# Vérifier si un point est à l'intérieur du cercle
def circle_contains(circle, point):
    return math.sqrt((circle.center.x - point.x) ** 2 + (circle.center.y - point.y) ** 2) <= circle.radius

# Calculer le cercle minimum englobant pour 1, 2 ou 3 points
def minidisk(points):
    if len(points) == 0:
        return None
    elif len(points) == 1:
        return Circle(points[0], 0)
    elif len(points) == 2:
        center_x = (points[0].x + points[1].x) / 2
        center_y = (points[0].y + points[1].y) / 2
        radius = math.sqrt((points[0].x - points[1].x) ** 2 + (points[0].y - points[1].y) ** 2) / 2
        return Circle(Point(center_x, center_y), radius)
    else:
        p1, p2, p3 = points
        center, radius = circumcircle(p1, p2, p3)
        return Circle(center, radius)

# Calculer le cercle circonscrit pour 3 points
def circumcircle(p1, p2, p3):
    ax, ay = p1.x, p1.y
    bx, by = p2.x, p2.y
    cx, cy = p3.x, p3.y
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    center = Point(ux, uy)
    radius = math.sqrt((ax - ux) ** 2 + (ay - uy) ** 2)
    return center, radius

# Lecture des points à partir d'un fichier
def read_points_from_file(file_path):
    points = []

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            values = line.strip().split()
            try:
                x, y = map(int, values)
                point = Point(x, y)
                points.append(point)
            except ValueError:
                continue
    return points

# Chemin du dossier contenant les fichiers de points
directory = 'Varoumas_benchmark/samples'

# Liste pour stocker les résultats
results = []

# Parcours des fichiers dans le dossier
for filename in os.listdir(directory):
    if filename.endswith('.points'):
        file_path = os.path.join(directory, filename)
        points = read_points_from_file(file_path)
        circle = welzl(points)
        result = [filename, len(points), circle.center.x, circle.center.y, circle.radius]
        results.append(result)

# Affichage des résultats
for result in results:
    print(f"Fichier : {result[0]}")
    print(f"Nombre de points : {result[1]}")
    print(f"Centre : ({result[2]}, {result[3]})")
    print(f"Rayon : {result[4]}")
    print()

