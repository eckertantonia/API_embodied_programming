from server.bolt import Bolt
from server.movement.movement_strategies.MovementStrategy import MovementStrategy


class InvitationStrategy(MovementStrategy):

    def drive(self, robots, points, initial_heading=None, offset=0):

        inviter = robots.bolts[0]
        invitee = robots.bolts[1]

        # inviter fährt nach vorne

        # inviter fährt zu invitee

        # inviter fährt zurück nach vorne

        # invitee folgt

        return
