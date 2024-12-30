import numpy as np
import matplotlib.pyplot as plt


import numpy as np
import time


def hermiteCurve(p0, p1, m0, m1, anzahl_punkte):
    """
    Berechnet eine hermitesche Kurve.

    Parameters:
        p0 (tuple): Startpunkt der Kurve (x0, y0).
        p1 (tuple): Endpunkt der Kurve (x1, y1).
        m0 (tuple): Tangentenvektor am Startpunkt (dx0, dy0).
        m1 (tuple): Tangentenvektor am Endpunkt (dx1, dy1).
        anzahl_punkte (int): Anzahl der Punkte auf der Kurve.

    Returns:
        list: Liste von Punkten (x, y) entlang der Kurve.
    """
     
    t = np.linspace(0, 1, anzahl_punkte)
    
    # Hermite-Basisfunktionen
    h00 = 2 * t**3 - 3 * t**2 + 1
    h10 = t**3 - 2 * t**2 + t
    h01 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2
    
    # Zerlege die Punkte und Tangenten
    x0, y0 = p0
    x1, y1 = p1
    dx0, dy0 = m0
    dx1, dy1 = m1
    
    # Berechne x und y entlang der Kurve
    x = h00 * x0 + h10 * dx0 + h01 * x1 + h11 * dx1
    y = h00 * y0 + h10 * dy0 + h01 * y1 + h11 * dy1
    
    return list(zip(x, y))

# Bewegungsbefehl berechnen
def calculate_commands(points):
    commands = []
    for i in range(1, len(points)):
        x1, y1 = points[i-1]
        x2, y2 = points[i]
        dx, dy = x2 - x1, y2 - y1
        distance = np.sqrt(dx**2 + dy**2) * 100  # Skalierung der Distanz
        angle = (np.degrees(np.arctan2(dy, dx)) + 360) % 360
        commands.append((distance, angle))
    return commands

if __name__ == "__main__":
    # Beispiel: Hermitesche Kurve
    p0 = (0, 0)       # Startpunkt
    p1 = (1, 1)       # Endpunkt
    m0 = (3, 0)       # Tangente am Start
    m1 = (0, 1)       # Tangente am Ende
    num_points = 100  # Anzahl der Punkte

    hermite_curve = hermiteCurve(p0, p1, m0, m1, num_points)

    # Zeichne die hermitesche Kurve
x, y = zip(*hermite_curve)
plt.plot(x, y, label="Hermite Curve", color="blue")

# Markiere die Kontrollpunkte und Tangenten
plt.scatter([p0[0], p1[0]], [p0[1], p1[1]], color="red", label="Control Points")
plt.quiver(*p0, *m0, color="green", angles='xy', scale_units='xy', scale=1, label="Start Tangent")
plt.quiver(*p1, *m1, color="orange", angles='xy', scale_units='xy', scale=1, label="End Tangent")

plt.title("Hermite Curve")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()

