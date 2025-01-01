import asyncio
from concurrent.futures import ThreadPoolExecutor

from spherov2.types import Color
from spherov2.sphero_edu import EventType


class FlockChoreo():
    def __init__(self, robots):
        self.broadcaster = robots[0]
        self.follower = robots[1]
        self.loop = asyncio.get_running_loop()
        self.executer = ThreadPoolExecutor()
        self.message_received_event = asyncio.Event()

    async def start_choreo(self):
        tasks = [
            self.task(self.start_broadcasting, self.broadcaster),
            self.task(self.start_following, self.follower)
        ]

        await asyncio.gather(*tasks)

    async def task(self, strategy, bolt):
        print("task")
        await self.loop.run_in_executor(self.executer, self.sync_task, strategy, bolt)

    def sync_task(self, strategy, bolt):
        try:
            with bolt.getApi() as bolt_api:
                bolt_api.set_matrix_character("|", color=Color(r=100, g=0, b=100))

                coro = strategy(bolt_api, bolt)
                asyncio.run_coroutine_threadsafe(coro, self.loop).result()

        except Exception as e:
            print(f"Error in sync_taks: {e}")
            raise

    async def start_broadcasting(self, robot, bolt):
        robot.start_ir_broadcast(0, 7)

        for i in range(5):
            robot_toy = robot._SpheroEduAPI__toy
            robot_toy.send_robot_to_robot_infrared_message(
                s=1,  # infrared_code Beispiel: "Ich bin hier"
                s2=64,   # IR-Stärke vorne (0-64)
                s3=0,     # Kein Signal nach links
                s4=0,    # Kein Signal nach rechts
                s5=0      # Kein Signal nach hinten
            )

            robot.send_ir_message(4, 10)
            print(f"send ir message {i}")
            await asyncio.sleep(5)

    async def start_following(self, robot, bolt):
        robot_toy = bolt
        data = []

        # Hier registrieren wir den IR-Nachricht-Listener
        def ir_message_listener(toy, message):
            print(f"IR Nachricht empfangen: {message}")
            self.message_received_event.set()  # Signalisiert, dass eine Nachricht empfangen wurde

        # Registriere den Listener für das 'on_ir_message' Event
        robot_toy.register_event(EventType.on_ir_message, ir_message_listener)

        # Starte die IR-Nachrichten-Verarbeitung und das Verfolgen
        robot_toy.toy.listen_for_robot_to_robot_infrared_message(s=1, j=0)
        robot.start_ir_follow(0, 7)

        # Warte, bis eine IR-Nachricht empfangen wird
        print("Warten auf IR-Nachricht...")
        await self.message_received_event.wait()

        print("IR-Nachricht empfangen und Event gesetzt.")

    def on_ir_message_received(self):
        print(f"message received")
        self.message_received_event.set()
