import math
import time

import matplotlib.pyplot as plt
import numpy as np


def calculate_hermite_curve(p0, p1, m0, m1, anzahl_punkte):
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
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1
    h10 = t ** 3 - 2 * t ** 2 + t
    h01 = -2 * t ** 3 + 3 * t ** 2
    h11 = t ** 3 - t ** 2

    # Punkte- und Tangenten-Tupel zerlegen
    x0, y0 = p0
    x1, y1 = p1
    dx0, dy0 = m0
    dx1, dy1 = m1

    # Berechne x und y entlang der Kurve
    x = h00 * x0 + h10 * dx0 + h01 * x1 + h11 * dx1
    y = h00 * y0 + h10 * dy0 + h01 * y1 + h11 * dy1

    return list(zip(x, y))


def calculate_hermite_spline(points, tangents, anzahl_punkte):
    """
    Berechnet einen Hermite-Spline durch mehrere Punkte.

    Parameters:
        points (list): Liste von Punkten [(x0, y0), (x1, y1), ...].
        tangents (list): Liste von Tangentenvektoren [(dx0, dy0), (dx1, dy1), ...].
        anzahl_punkte (int): Anzahl der Punkte pro Segment.

    Returns:
        list: Liste von Punkten (x, y) entlang des Splines.
    """
    if len(points) < 2 or len(points) != len(tangents):
        raise ValueError("Die Anzahl der Punkte und Tangenten muss gleich sein und mindestens 2 Punkte enthalten.")

    spline_points = []

    for i in range(len(points) - 1):
        # Extrahiere Start- und Endpunkte sowie Tangenten des aktuellen Segments
        p0 = points[i]
        p1 = points[i + 1]
        m0 = tangents[i]
        m1 = tangents[i + 1]

        # Berechne die Punkte der Hermite-Kurve für das aktuelle Segment
        segment_points = calculate_hermite_curve(p0, p1, m0, m1, anzahl_punkte)

        # Füge die Punkte zur Gesamtliste hinzu, vermeide doppelte Punkte an Segmentgrenzen
        if i > 0:
            segment_points = segment_points[1:]
        spline_points.extend(segment_points)

    return spline_points


def calculate_tangents(points, initial_heading=None):
    """
    Berechnet Tangentenvektoren für eine gegebene Liste von Punkten.

    Parameters:
        points (list): Liste von Punkten [(x0, y0), (x1, y1), ...].
        initial_heading (float, optional): Ausrichtung in Grad am Startpunkt

    Returns:
        list: Liste von Tangenten [(dx0, dy0), (dx1, dy1), ...].
    """
    tangents = []
    n = len(points)

    for i in range(n):
        if i == 0:  # Vorwärtsdifferenz am Anfang
            if initial_heading is not None:
                # Initialer Tangentenvektor basierend auf der Orientierung
                angle_deg = initial_heading
                dx = math.cos(math.radians(angle_deg))
                dy = math.sin(math.radians(angle_deg))
            else:
                # Vorwärtsdifferenz, wenn keine Orientierung gegeben ist
                dx, dy = points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1]
        elif i == n - 1:  # Rückwärtsdifferenz am Ende
            dx, dy = points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1]
        else:  # Zentrale Differenz für mittlere Punkte
            dx = (points[i + 1][0] - points[i - 1][0]) / 2
            dy = (points[i + 1][1] - points[i - 1][1]) / 2
        tangents.append((dx, dy))

    return tangents


# Bewegungsbefehl berechnen
def calculate_commands(points, compass_offset):
    """
    Berechnet Bewegungsbefehle basierend auf Punkten.

    Parameters:
        points (list): Liste von Punkten [(x0, y0), (x1, y1), ...].
        compass_offset (float): Offset des Roboters im globalen Koordinatensystem (in Grad).

    Returns:
        list: Liste von Bewegungsbefehlen [(distance, angle_in_degrees), ...].
    """
    commands = []
    for i in range(1, len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]
        dx, dy = x2 - x1, y2 - y1
        distance = (np.sqrt(dx ** 2 + dy ** 2)) * 20  # Mit Skalierung
        angle = (360 - math.degrees(math.atan2(dy, dx))) % 360
        # Transformiere Winkel ins globale Koordinatensystem
        global_angle = (angle + compass_offset) % 360
        commands.append((int(distance), int(global_angle)))
    return commands


# Sphero Bolt fahren lassen
def drive_hermite_curve(robot, points, initial_heading=None):
    """
    Fährt eine Hermite-Kurve mit dem Roboter.

    Parameters:
        robot: Der Roboter, der die Bewegung ausführt.
        points (list): Liste von Punkten [(x0, y0), (x1, y1), ...].
        speed (int): Geschwindigkeit der Bewegung.
        initial_heading (float): Anfangsrichtung des Roboters.
        compass_offset (float): Offset des Roboters im globalen Koordinatensystem (in Grad).

    Returns:
        None
    """
    try:
        tangents = calculate_tangents(points, initial_heading=initial_heading)

        spline = calculate_hermite_spline(points, tangents, len(points))
        # commands = calculate_commands(spline, compass_offset=compass_offset)
        commands = calculate_commands(points, compass_offset=robot.offset)

        _basic_drive(robot.toy_api, commands)
        robot.update_position(points[-1])
    except Exception as e:
        print(f"Exception in drive_hermite_curve: {e}")
        raise


def _basic_drive(robot_api, commands, speed=50):
    """
    TODO: speed 50 ist ein bisschen sehr gemaechlich
    holt Schwung und bremst ab
    :param robot_api:
    :param commands:
    :return:
    """

    # Gesamtdistanz berechnen
    total_distance = 0
    for i in commands:
        total_distance += i[0]

    calculated_distance = total_distance  # in cm

    # Falls die Distanz 0 ist, beende die Funktion
    if total_distance == 0:
        print("Gesamtdistanz ist 0. Keine Bewegung erforderlich.")
        return

    first_distance, first_angle = commands[0]

    robot_api.roll(first_angle, 0, 1)
    start_distance = robot_api.get_distance()

    control_distance(robot_api, commands, speed)


def control_distance(robot, commands, speed):
    """
    Kontrolliert den Roboter basierend auf den Befehlen und passt das Heading an.
    """

    for distance, angle in commands:
        time.sleep(0.5)
        robot.set_heading(angle)
        print(f"{robot._SpheroEduAPI__toy.name}{angle}")
        time.sleep(0.5)
        start_distance = robot.get_distance()  # robot setzt heading
        cur_distance = 0
        robot.set_speed(speed)
        while cur_distance < distance - 4:
            cur_distance = robot.get_distance() - start_distance  # robot faehrt bis distance erreicht
            time.sleep(0.01)

        robot.set_speed(0)
        stop_distance = robot.get_distance() - start_distance
        # Start fuer naechsten Abschnitt

    robot.set_speed(0)  # Anhalten, wenn alle Kommandos abgearbeitet sind


def plotSpline(points, initial_heading):
    """
    Plottet den berechneten Hermite-Spline mit Kontrollpunkten und Tangenten.

    Parameters:
        points (list): Liste von Kontrollpunkten [(x0, y0), (x1, y1), ...].
        tangents (list): Liste von Tangenten [(dx0, dy0), (dx1, dy1), ...].
        spline_points (list): Liste von Punkten auf dem Spline [(x, y), ...].
        initial_heading:
    """

    tangents = calculate_tangents(points, initial_heading=initial_heading)
    spline_points = calculate_hermite_spline(points, tangents, 10)

    # Kontrollpunkte und Tangenten plotten
    for i, (point, tangent) in enumerate(zip(points, tangents)):
        plt.plot(point[0], point[1], 'ro')  # Kontrollpunkt
        plt.arrow(point[0], point[1], tangent[0] * 0.1, tangent[1] * 0.1, color='r', head_width=0.05)

    # Spline plotten
    spline_x, spline_y = zip(*spline_points)
    plt.plot(spline_x, spline_y, 'b-', label='Hermite-Spline')

    # Kontrollpunkte verbinden
    control_x, control_y = zip(*points)
    plt.plot(control_x, control_y, 'g--', label='Kontrollpunkte')

    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Hermite-Spline mit Kontrollpunkten und Tangenten')
    plt.axis('equal')
    plt.grid(True)
    plt.savefig("splinePlot.png")
    # plt.show()
    plt.close()
    print("plotted")
