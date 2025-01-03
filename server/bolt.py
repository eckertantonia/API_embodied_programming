import time

from spherov2.sphero_edu import SpheroEduAPI, EventType

import threading


class Bolt:
    def __init__(self, toy):
        self.name = toy.name
        self.toy = toy
        self.toyApi = SpheroEduAPI(self.toy)  # API für den Sphero Toy initialisieren
        self.listeners = {EventType.on_ir_message: []}  # Event-Listener für IR-Nachrichten
        self.position = (0, 0)  # Standard-Startposition
        self.offset = 0 # Default 0, TODO berechnen

    def update_position(self, new_pos):
        """Aktualisiert die Postion des Bolt."""
        self.position = new_pos

    def get_spheroeduapi(self) -> SpheroEduAPI:
        """Gibt die SpheroEduApi-Instanz zu diesem Bolt zurück."""
        try:
            return self.toyApi
        except Exception as e:
            print(f"Exception in Bolt.get_spheroeduapi: {e}")
            raise

    def calibrate(self, running_api):
        running_api.calibrate_compass()
        self.offset = running_api._SpheroEduAPI__compass_zero
        time.sleep(2)

        # running_api.set_compass_direction(0)
        #self.calculate_offset()

    def calculate_offset(self):
        offset = 0 - self.toyApi._SpheroEduAPI__compass_zero
        self.offset = (offset) % 360
        print(f"{self.name} offset: {self.offset}")

# TODO prüfen, ob gebraucht wird
    def register_event(self, event_type: EventType, listener: callable):
        """Registriert einen Event-Listener für ein bestimmtes Event."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def _call_event_listener(self, event_type: EventType, *args, **kwargs):
        """Benachrichtigt alle registrierten Listener für das Event."""
        for listener in self.listeners.get(event_type, []):
            threading.Thread(target=listener, args=(self.toyApi, *args), kwargs=kwargs).start()

    def listen_for_ir_messages(self):
        """Simuliert das Warten auf IR-Nachrichten und löst das Event aus."""

        def on_message_received(message):
            print(f"IR-Nachricht empfangen: {message}")
            self._call_event_listener(EventType.on_ir_message, message)

        # Registriere die Methode, die auf IR-Nachrichten reagiert
        self.toyApi.register_event(EventType.on_ir_message, on_message_received)