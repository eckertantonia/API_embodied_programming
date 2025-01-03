import asyncio
import math
import time
from concurrent.futures import ThreadPoolExecutor

from server.movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy

from spherov2.types import Color


class FlockChoreo():
    def __init__(self, robots):
        self.bolts = robots
        self.leader = None
        self.follower = []
        self.loop = asyncio.get_running_loop()
        self.executer = ThreadPoolExecutor()
        self.leader_pos_event = asyncio.Event()
        self.leader_location = None
        self.leader_heading = None
        self.scale = 20  # cm, 20cm = 1 Einheit internes Koordinatensystem TODO: config-file

    async def start_choreo(self):

        self.assign_pos()

        flock_tasks = [
                          self.task(self.start_leader, self.leader)
                      ] + [
                          self.task(self.start_following, following) for following in self.follower
                      ]

        await asyncio.gather(*flock_tasks)

    def assign_pos(self):
        positions = [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]
        # positions = [(0, 0),(0, -1)]

        for bolt in self.bolts:
            if bolt.name == "SB-E118":
                bolt.update_position(positions[0])
                self.leader = bolt
                self.leader_location = bolt.position
            elif bolt.name == "SB-DAC2":
                bolt.update_position(positions[1])
                self.follower.append(bolt)
            elif bolt.name == "SB-F545":
                bolt.update_position(positions[2])
                self.follower.append(bolt)
            elif bolt.name == "SB-6476":
                bolt.update_position(positions[3])
                self.follower.append(bolt)
            elif bolt.name == "SB-34D5":
                bolt.update_position(positions[4])
                self.follower.append(bolt)

    async def task(self, strategy, bolt):
        await self.loop.run_in_executor(self.executer, self.sync_task, strategy, bolt)

    def sync_task(self, strategy, bolt):
        # synchrone Methode, weil SpheroEduApi synchron ist
        try:
            with bolt.get_spheroeduapi() as bolt_api:
                bolt_api.calibrate_compass()
                time.sleep(2)
                bolt_api.set_compass_direction(0)
                bolt_api.reset_aim()

                strategy = strategy(bolt_api, bolt)
                asyncio.run_coroutine_threadsafe(strategy, self.loop).result()

        except asyncio.TimeoutError as timeout:
            print(f"TimeoutError in sync_task for Bolt {bolt.name}: {timeout}")
        except Exception as e:
            print(f"Error in sync_taks: {e}")
            raise

    async def start_leader(self, robot, bolt):
        try:
            robot.set_matrix_character("L", color=Color(r=100, g=0, b=100))

            self.leader_location = bolt.position
            self.leader_heading = robot.get_heading()
            print(f"leader location: {self.leader_location}")
            await asyncio.sleep(30)
        except Exception as e:
            print(f"Exception in start_leader with Bolt {bolt.name}: {e}")

    async def start_following(self, robot, bolt):
        try:
            robot.set_matrix_character("F", color=Color(r=100, g=0, b=0))

            print(f"Bolt {bolt.name} an Pos {bolt.position}")

            move = MoveForwardStrategy()

            if self.leader_location is not None:

                route_points = [bolt.position, self.leader_location]
                robot.set_matrix_character("F", color=Color(r=0, g=100, b=0))
                await asyncio.sleep(3)

                move.drive(robot, route_points, initial_heading=robot.get_heading())
                print("i roll...")
                await asyncio.sleep(10)
            else:
                print("No leader")
        except Exception as e:
            print(f"Exception in start_following with Bolt {bolt.name}: {e}")

    async def navigate_to_leaderpos(self, cur_pos):
        speed_cm_per_sec = 40

        x1, y1 = cur_pos[0], cur_pos[1]
        x2, y2 = self.leader_location[0], self.leader_location[1]

        # Berechnung Distanz
        distance_units = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        distance_cm = distance_units * self.scale

        # Berechnung Winkel (heading)
        # TODO: die Winkel sich wack
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        if angle < 0:
            angle += 360  # damit Winkel zwischen 0 und 360

        # Zeit
        duration = distance_cm / speed_cm_per_sec

        speed = int(speed_cm_per_sec / speed_cm_per_sec * 255)
        speed = max(min(speed, 255), 0)

        return int(angle), speed, duration
