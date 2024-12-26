import numpy as np
import time

from bolt import Bolt
from spherov2.types import Color

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
    # gleichmaessig verteiltes array mit num werten zwischen start und stop
    # erzeugt werte fuer t entlang der kurve, 
    # t ist array aus werten
    t = np.linspace(0, 1, anzahl_punkte)
    
    # Hermite-Basisfunktionen
    h00 = 2 * t**3 - 3 * t**2 + 1
    h10 = t**3 - 2 * t**2 + t
    h01 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2
    
    # Punkte- und Tangenten-Tupel zerlegen
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

# Sphero Bolt fahren lassen
def drive_hermite_curve(robot, commands, speed=50):
    # TODO LED auslagern
    
    for distance, angle in commands:
        robot.set_matrix_character("|", color=Color(r=100, g=0, b=100))
        robot.roll(int(angle), speed, (distance/speed))
       # time.sleep(distance / speed)  # Warte proportional zur Strecke
        robot.set_matrix_character("|", color=Color(r=0, g=100, b=100))

