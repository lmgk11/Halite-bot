import logging
import hlt
from collections import OrderedDict

game = hlt.Game("Milo")
logging.info("Starting Milo")

while True:
    my_ships = game_map.get_me().all_ships()

    game_map = game.update_map()
    command_queue = []

    for ship in my_ships:
        ship_id = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
        closest_empty_planet = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        if len(closest_empty_planets) > 0 and ship.can_dock(closest_empty_planets[0]):
            command_queue.append(ship.dock(closest_empty_planet[0]))
        else:
            navigate_command = ship.navigate(
                ship.closest_point_to(planet),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=True)
        if navigate_command:
            command_queue.append(navigate_command)
    game.send_command_queue(command_queue)
