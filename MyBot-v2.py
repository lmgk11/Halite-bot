import logging
import hlt
from collections import OrderedDict

game = hlt.Game("Milo")
logging.info("Starting Milo")

def Attack(my_planets, ships):
    for planet in my_planets:
        for ship in ships:
            if calculate_distance_between(ship, planet) < 14:
                return ship

    return None;

while True:
    game_map = game.update_map()

    command_queue = []

    for ship in game_map.get_me().all_ships():
        ship_id = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        my_ships = game_map.get_me().all_ships()
        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_ships]

        my_planets = []

        attack_specific_ship = Attack(my_planets, closest_enemy_ships)

        if attack_specific_ship != None:
            navigate_command = ship.navigate(
                ship.closest_point_to(attack_specific_ship),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=True)
            if navigate_command:
                command_queue.append(navigate_command)
        else:
            if len(closest_empty_planets) > 0:
                if (ship.can_dock(closest_empty_planets[0])):
                    command_queue.append(ship.dock(closest_empty_planets[0]))
                    my_planets.append(closest_empty_planets[0])
                else:
                    navigate_command = ship.navigate(
                        ship.closest_point_to(closest_empty_planets[0]),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=True)
                    if navigate_command:
                        command_queue.append(navigate_command)
            if len(closest_enemy_ships) > 0 and len(closest_empty_planets) == 0:
                navigate_command = ship.navigate(
                    ship.closest_point_to(closest_enemy_ships[0]),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=True)
                if navigate_command:
                    command_queue.append(navigate_command)
    game.send_command_queue(command_queue)
