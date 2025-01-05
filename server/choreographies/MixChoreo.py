from sqlite3.dbapi2 import apilevel

from server.movement.movement_strategies.MovementInterface import MovementInterface


class MixChoreo:

    async def start_choreo(self, bolt_group, strategy:MovementInterface):

        # 2 bolts aus bolt_group fuer circle
        target_names = {"SB-E118", "SB-DAC2"} # testzwecke

        filtered_bolts = {
            bolt:api for bolt, api in bolt_group.items() if bolt.toy in target_names
        }

        print(f"filtered_bolts: {filtered_bolts}")

        await strategy.drive(filtered_bolts, [])
