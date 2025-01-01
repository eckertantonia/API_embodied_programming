import asyncio
import math
from concurrent.futures import ThreadPoolExecutor

from spherov2.types import Color
from spherov2.sphero_edu import EventType
import server.movement.basics as basic_moves

class FlockChoreo():
    def __init__(self, robots):
        self.broadcaster = robots[0]
        self.follower = robots[1]
        self.loop = asyncio.get_running_loop()
        self.executer = ThreadPoolExecutor()
        self.leader_pos_event = asyncio.Event()
        self.leader_location = None
        self.leader_heading = None
        self.scale = 20 #cm, 20cm = 1 Einheit internes Koordinatensystem

    async def start_choreo(self):
        tasks = [
            self.task(self.start_leader, self.broadcaster),
            self.task(self.start_following, self.follower)
        ]

        await asyncio.gather(*tasks)

    async def task(self, strategy, bolt):
        print("task")
        await self.loop.run_in_executor(self.executer, self.sync_task, strategy, bolt)

    def sync_task(self, strategy, bolt):
        try:
            with bolt.getApi() as bolt_api:
                bolt_api.calibrate_compass()
                bolt_api.set_compass_direction(0)
                bolt_api.set_matrix_character("|", color=Color(r=100, g=0, b=100))

                coro = strategy(bolt_api, bolt)
                asyncio.run_coroutine_threadsafe(coro, self.loop).result()

        except Exception as e:
            print(f"Error in sync_taks: {e}")
            raise

    async def start_leader(self, robot, bolt):
        robot.set_matrix_character("L", color=Color(r=100, g=0, b=100))
        await asyncio.sleep(20)
        bolt.set_pos(0, 0)
        self.leader_location = bolt.pos
        self.leader_heading = robot.get_heading()
        print(f"leader location: {self.leader_location}")
        print(f"leader compass direction: {robot.get_compass_direction()}")
        self.leader_pos_event.set()
        await asyncio.sleep(30)

    async def start_following(self, robot, bolt):
        robot.set_matrix_character("F", color=Color(r=100, g=0, b=0))
        await asyncio.sleep(10)
        robot.set_matrix_character("F", color=Color(r=0, g=100, b=0))
        bolt.set_pos(1, 1)
        location = robot.get_location()
        while location is math.nan:
            location = robot.get_location()
            if location is not math.nan:
                break
        heading = robot.get_heading()
        points = [bolt.pos, (bolt.pos[0]+1, bolt.pos[1]), bolt.pos]
        #basic_moves.drive_hermite_curve(robot, points)
        await self.leader_pos_event.wait()
        angle, speed, duration = await self.navigate_to_leaderpos(bolt.pos)

        robot.roll(angle, speed, 2)
        print("i roll...")
        await asyncio.sleep(20)

    async def navigate_to_leaderpos(self, cur_pos):
        speed_cm_per_sec = 40

        x1, y1 = cur_pos[0], cur_pos[1]
        x2, y2 = self.leader_location[0], self.leader_location[1]

        # Berechnung Distanz
        distance_units = math.sqrt((x2-x1)**2 + (y2-y1)**2)

        distance_cm = distance_units * self.scale

        # Berechnung Winkel (heading)
        # TODO: die Winkel sich wack
        angle = math.degrees(math.atan2(y2-y1, x2-x1))
        if angle < 0:
            angle += 360 # damit Winkel zwischen 0 und 360

        # Zeit
        duration = distance_cm / speed_cm_per_sec

        speed = int(speed_cm_per_sec / speed_cm_per_sec * 255)
        speed = max(min(speed, 255), 0)

        return int(angle), speed, duration
