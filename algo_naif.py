import math
import time
import csv
import os

# Définition de la structure de point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Définition de la structure de cercle
class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

# Calcul de la distance euclidienne entre deux points
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# Vérifier si un point est contenu dans le cercle
def point_inside_circle(circle, point):
    return distance(circle.center, point) <= circle.radius

# Algorithme naïf de cercle minimum
def naive_minimum_circle(points):
    n = len(points)

    if n == 0:
        return None

    if n == 1:
        return Circle(points[0], 0)

    if n == 2:
        center_x = (points[0].x + points[1].x) / 2
        center_y = (points[0].y + points[1].y) / 2
        radius = distance(points[0], points[1]) / 2
        return Circle(Point(center_x, center_y), radius)

    min_circle = None

    for i in range(n):
        for j in range(i + 1, n):
            circle = create_circle(points[i], points[j])

            if circle is None:
                continue

            points_inside = True

            for k in range(n):
                if k != i and k != j and not point_inside_circle(circle, points[k]):
                    points_inside = False
                    break

            if points_inside and (min_circle is None or circle.radius < min_circle.radius):
                min_circle = circle

    return min_circle

# Créer un cercle à partir de deux points
def create_circle(p1, p2):
    center_x = (p1.x + p2.x) / 2
    center_y = (p1.y + p2.y) / 2
    radius = distance(p1, p2) / 2

    for i in range(len(points)):
        point = points[i]
        if not point_inside_circle(Circle(Point(center_x, center_y), radius), point):
            return None

    return Circle(Point(center_x, center_y), radius)


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




# Enregistrement des résultats dans un fichier CSV
def save_results_to_csv(results):
    with open('resultat.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Fichier', 'Compteur', 'Temps d\'exécution'])

        for result in results:
            writer.writerow(result)

# Chemin du dossier contenant les fichiers
folder_path = 'Varoumas_benchmark/samples'

# Liste des chemins complets des fichiers dans le dossier
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.points')]

results = []

for file_path in file_paths:
    points = read_points_from_file(file_path)

    start_time = time.time()
    circle = naive_minimum_circle(points)
    end_time = time.time()

    execution_time = end_time - start_time
    point_count = len(points)

    results.append([os.path.basename(file_path), point_count, execution_time])  # Ajout du nom du fichier

    print("Fichier :", file_path)
    if circle is not None:
        print("Centre :", circle.center.x, circle.center.y)
        print("Rayon :", circle.radius)
    else:
        print("Aucun cercle trouvé.")

save_results_to_csv(results)
