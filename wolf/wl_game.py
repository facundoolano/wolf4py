# TODO
import id_cache as id_ca
import wl_def as de
import wl_play as wl_play
import id_input as id_in

class GameState():
    difficulty = 2
    mapon = 0
    lives = 3
    health = 100
    ammo = de.START_AMMO
    keys = 0

    weapon = de.WP_PISTOL
    best_weapon = de.WP_PISTOL
    chosen_weapon = de.WP_PISTOL

    faceframe = 0
    attackframe = 0
    attackcount = 0
    weaponframe = 0

    episode = 0
    secretcount = 0
    treasurecount = 0
    killcount = 0
    secrettotal = 0
    treasuretotal = 0
    killtotal = 0

    time_count = 0
    kill_x = 0
    kill_y = 0

    # defined in wl_play in wolf4sdl
    actorat = [[0 for _ in range(de.MAP_HEIGHT)]
               for _ in range(de.MAP_WIDTH)]
    tilemap = [[0 for _ in range(de.MAP_HEIGHT)]
               for _ in range(de.MAP_WIDTH)]

state = GameState()

def loop():
    # TODO this is originally inside the loop
    setup_game_level()

    wl_play.loop()
    # TODO this should be a loop, for now just draw once and wait for input to quit
    id_in.user_input()


def setup_game_level():
    # load the level
    id_ca.cache_map(state.mapon + 10 * state.episode)

    # copy the wall data to a data segment array
    tiles = iter(id_ca.state.mapsegs[0])
    for y in range(de.MAP_HEIGHT):
        for x in range(de.MAP_WIDTH):

            tile = next(tiles)
            if tile < de.AREA_TILE:
                # solid wall
                state.tilemap[x][y] = tile

                # FIXME what's this pointer thingy?
                # TODO figure out how actorat is used.
                # may need to wrap into object to share state
                # actorat[x][y] = (objtype *)(uintptr_t) tile
                state.actorat[x][y] = tile

    # start spawning things with a clean slate
    # init_actor_list()
    # init_doorl_list()
    # init_static_list()

    # TODO reduce duplication?
    # TODO do the init funs above change the tiles? could we init all together?
    tiles = iter(id_ca.state.mapsegs[0])
    for y in range(de.MAP_HEIGHT):
        for x in range(de.MAP_WIDTH):
            tile = next(tiles)

            if tile in [90, 92, 94, 96, 98, 100]:
                # TODO spawn_door(x, y, 1, (tile - 90) // 2)
                pass
            elif tile in [91, 93, 95, 97, 99, 101]:
                # TODO spawn_door(x, y, 0, (tile - 91) // 2)
                pass

    # spwan actors
    # TODO rename?
    scan_info_plane()

    # take out the ambush markers
    mapsegs = id_ca.state.mapsegs[0]
    for y in range(de.MAP_HEIGHT):
        for x in range(de.MAP_WIDTH):

            idx = y + x
            tile = mapsegs[idx]
            idx += 1
            if tile == de.AMBUSH_TILE:
                tilemap[x][y] = 0

                if actorat[x][y] == de.AMBUSH_TILE:
                    state.actorat[x][y] = None

                if mapsegs[idx] >= AREATILE:
                    tile = mapsegs[idx]
                if mapsegs[idx -1 - de.MAP_WIDTH] >= AREATILE:
                    tile = mapsegs[idx -1 - de.MAP_WIDTH]
                if mapsegs[idx -1 + de.MAP_WIDTH] >= AREATILE:
                    tile = mapsegs[idx -1 + de.MAP_WIDTH]
                if mapsges[idx-2] >= AREATILE:
                    tile = mapsges[idx-2]

                mapsges[idx-1] = tile

def scan_info_plane():
    # TODO this sets up enemies
    pass
