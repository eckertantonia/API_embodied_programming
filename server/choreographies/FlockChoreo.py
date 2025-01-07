import asyncio
import math
import time
from concurrent.futures import ThreadPoolExecutor

from spherov2.sphero_edu import SpheroEduAPI

from server.movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy

from spherov2.types import Color

# TODO: Logik in Strategy schieben
# Choreo nur dafür da um Strategies aneinander zu hängen

class FlockChoreo:
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
        """
        Zuweisung von Task zu Bolt
        :return:
        """

        self.assign_pos() # später unwichtig, weil position schon in bolt gespeichert

        flock_tasks = [
                          self.task(self.start_leader, self.leader)
                      ] + [
                          self.task(self.start_following, following) for following in self.follower
                      ]

        await asyncio.gather(*flock_tasks)

    def assign_pos(self):

        # TODO: vorerst Helfer, muss an endgültige Choreo angepasst werden.
        positions = [(0, 0), (0, 2), (2, 0), (0, -2), (-2, 0)]
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
            # Bolt kalibrieren, Offset setzen
            bolt.calibrate()

            strategy = strategy(bolt)

            #TODO: ist das Thread oder Coroutine?
            asyncio.run_coroutine_threadsafe(strategy, self.loop).result()

        except asyncio.TimeoutError as timeout:
            print(f"TimeoutError in sync_task for Bolt {bolt.name}: {timeout}")
        except Exception as e:
            print(f"{bolt.name} Error in sync_taks: {e}")

    async def start_leader(self, bolt):
        try:
            bolt.toyApi.set_matrix_character("L", color=Color(r=100, g=0, b=100))

            self.leader_location = bolt.position
            self.leader_heading = bolt.toyApi.get_heading()
            print(f"leader location: {self.leader_location}")
            await asyncio.sleep(30)
        except Exception as e:
            print(f"Exception in start_leader with Bolt {bolt.name}: {e}")

    async def start_following(self, bolt):
        try:
            bolt.toyApi.set_matrix_character("F", color=Color(r=100, g=0, b=0))

            print(f"Bolt {bolt.name} an Pos {bolt.position}")

            move = MoveForwardStrategy()

            if self.leader_location is not None:
                # Route setzen
                route_points = [bolt.position, self.leader_location]
                bolt.toyApi.set_matrix_character("F", color=Color(r=0, g=100, b=0))
                await asyncio.sleep(3)
                print(f"{bolt.name} position {bolt.position}")
                # Route fahren
                move.drive(bolt.toyApi, route_points, offset=bolt.offset)
                print(f"{bolt.name} roll...")
                # Position updaten
                bolt.update_position(route_points[-1])
                print(f"{bolt.name} position {bolt.position}")
                await asyncio.sleep(10)
            else:
                print("No leader")
        except Exception as e:
            print(f"Exception in start_following with Bolt {bolt.name}: {e}")
