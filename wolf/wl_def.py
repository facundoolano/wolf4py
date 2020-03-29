from enum import Enum

STATUS_LINES = 40

MAP_SIZE = 64
MAP_AREA = MAP_SIZE * MAP_SIZE
MAP_HEIGHT = MAP_SIZE
MAP_WIDTH = MAP_SIZE

AMBUSH_TILE = 106
AREA_TILE = 107         # first of NUMAREAS floor tiles

START_AMMO = 8
WP_KNIFE = 0
WP_PISTOL = 1
WP_MACHINEGUN = 2
WP_CHAINGUN = 3

SPRITE_SCALE_FACTOR = 2

Sprites = Enum('Sprites', [
    'DEMO', 'DEATHCAM',
    # static sprites
    'STAT_0', 'STAT_1', 'STAT_2', 'STAT_3',
    'STAT_4', 'STAT_5', 'STAT_6', 'STAT_7',
    'STAT_8', 'STAT_9', 'STAT_10', 'STAT_11',
    'STAT_12', 'STAT_13', 'STAT_14', 'STAT_15',
    'STAT_16', 'STAT_17', 'STAT_18', 'STAT_19',
    'STAT_20', 'STAT_21', 'STAT_22', 'STAT_23',
    'STAT_24', 'STAT_25', 'STAT_26', 'STAT_27',
    'STAT_28', 'STAT_29', 'STAT_30', 'STAT_31',
    'STAT_32', 'STAT_33', 'STAT_34', 'STAT_35',
    'STAT_36', 'STAT_37', 'STAT_38', 'STAT_39',
    'STAT_40', 'STAT_41', 'STAT_42', 'STAT_43',
    'STAT_44', 'STAT_45', 'STAT_46', 'STAT_47',
    # guard
    'GRD_S_1', 'GRD_S_2', 'GRD_S_3', 'GRD_S_4',
    'GRD_S_5', 'GRD_S_6', 'GRD_S_7', 'GRD_S_8',
    'GRD_W1_1', 'GRD_W1_2', 'GRD_W1_3', 'GRD_W1_4',
    'GRD_W1_5', 'GRD_W1_6', 'GRD_W1_7', 'GRD_W1_8',
    'GRD_W2_1', 'GRD_W2_2', 'GRD_W2_3', 'GRD_W2_4',
    'GRD_W2_5', 'GRD_W2_6', 'GRD_W2_7', 'GRD_W2_8',
    'GRD_W3_1', 'GRD_W3_2', 'GRD_W3_3', 'GRD_W3_4',
    'GRD_W3_5', 'GRD_W3_6', 'GRD_W3_7', 'GRD_W3_8',
    'GRD_W4_1', 'GRD_W4_2', 'GRD_W4_3', 'GRD_W4_4',
    'GRD_W4_5', 'GRD_W4_6', 'GRD_W4_7', 'GRD_W4_8',
    'GRD_PAIN_1', 'GRD_DIE_1', 'GRD_DIE_2', 'GRD_DIE_3',
    'GRD_PAIN_2', 'GRD_DEAD',
    'GRD_SHOOT1', 'GRD_SHOOT2', 'GRD_SHOOT3',
    # dogs
    'DOG_W1_1', 'DOG_W1_2', 'DOG_W1_3', 'DOG_W1_4',
    'DOG_W1_5', 'DOG_W1_6', 'DOG_W1_7', 'DOG_W1_8',
    'DOG_W2_1', 'DOG_W2_2', 'DOG_W2_3', 'DOG_W2_4',
    'DOG_W2_5', 'DOG_W2_6', 'DOG_W2_7', 'DOG_W2_8',
    'DOG_W3_1', 'DOG_W3_2', 'DOG_W3_3', 'DOG_W3_4',
    'DOG_W3_5', 'DOG_W3_6', 'DOG_W3_7', 'DOG_W3_8',
    'DOG_W4_1', 'DOG_W4_2', 'DOG_W4_3', 'DOG_W4_4',
    'DOG_W4_5', 'DOG_W4_6', 'DOG_W4_7', 'DOG_W4_8',
    'DOG_DIE_1', 'DOG_DIE_2', 'DOG_DIE_3', 'DOG_DEAD',
    'DOG_JUMP1', 'DOG_JUMP2', 'DOG_JUMP3',
    # ss
    'SS_S_1', 'SS_S_2', 'SS_S_3', 'SS_S_4',
    'SS_S_5', 'SS_S_6', 'SS_S_7', 'SS_S_8',
    'SS_W1_1', 'SS_W1_2', 'SS_W1_3', 'SS_W1_4',
    'SS_W1_5', 'SS_W1_6', 'SS_W1_7', 'SS_W1_8',
    'SS_W2_1', 'SS_W2_2', 'SS_W2_3', 'SS_W2_4',
    'SS_W2_5', 'SS_W2_6', 'SS_W2_7', 'SS_W2_8',
    'SS_W3_1', 'SS_W3_2', 'SS_W3_3', 'SS_W3_4',
    'SS_W3_5', 'SS_W3_6', 'SS_W3_7', 'SS_W3_8',
    'SS_W4_1', 'SS_W4_2', 'SS_W4_3', 'SS_W4_4',
    'SS_W4_5', 'SS_W4_6', 'SS_W4_7', 'SS_W4_8',
    'SS_PAIN_1', 'SS_DIE_1', 'SS_DIE_2', 'SS_DIE_3',
    'SS_PAIN_2', 'SS_DEAD',
    'SS_SHOOT1', 'SS_SHOOT2', 'SS_SHOOT3',
    # mutant
    'MUT_S_1', 'MUT_S_2', 'MUT_S_3', 'MUT_S_4',
    'MUT_S_5', 'MUT_S_6', 'MUT_S_7', 'MUT_S_8',
    'MUT_W1_1', 'MUT_W1_2', 'MUT_W1_3', 'MUT_W1_4',
    'MUT_W1_5', 'MUT_W1_6', 'MUT_W1_7', 'MUT_W1_8',
    'MUT_W2_1', 'MUT_W2_2', 'MUT_W2_3', 'MUT_W2_4',
    'MUT_W2_5', 'MUT_W2_6', 'MUT_W2_7', 'MUT_W2_8',
    'MUT_W3_1', 'MUT_W3_2', 'MUT_W3_3', 'MUT_W3_4',
    'MUT_W3_5', 'MUT_W3_6', 'MUT_W3_7', 'MUT_W3_8',
    'MUT_W4_1', 'MUT_W4_2', 'MUT_W4_3', 'MUT_W4_4',
    'MUT_W4_5', 'MUT_W4_6', 'MUT_W4_7', 'MUT_W4_8',
    'MUT_PAIN_1', 'MUT_DIE_1', 'MUT_DIE_2', 'MUT_DIE_3',
    'MUT_PAIN_2', 'MUT_DIE_4', 'MUT_DEAD',
    'MUT_SHOOT1', 'MUT_SHOOT2', 'MUT_SHOOT3', 'MUT_SHOOT4',
    # officer
    'OFC_S_1', 'OFC_S_2', 'OFC_S_3', 'OFC_S_4',
    'OFC_S_5', 'OFC_S_6', 'OFC_S_7', 'OFC_S_8',
    'OFC_W1_1', 'OFC_W1_2', 'OFC_W1_3', 'OFC_W1_4',
    'OFC_W1_5', 'OFC_W1_6', 'OFC_W1_7', 'OFC_W1_8',
    'OFC_W2_1', 'OFC_W2_2', 'OFC_W2_3', 'OFC_W2_4',
    'OFC_W2_5', 'OFC_W2_6', 'OFC_W2_7', 'OFC_W2_8',
    'OFC_W3_1', 'OFC_W3_2', 'OFC_W3_3', 'OFC_W3_4',
    'OFC_W3_5', 'OFC_W3_6', 'OFC_W3_7', 'OFC_W3_8',
    'OFC_W4_1', 'OFC_W4_2', 'OFC_W4_3', 'OFC_W4_4',
    'OFC_W4_5', 'OFC_W4_6', 'OFC_W4_7', 'OFC_W4_8',
    'OFC_PAIN_1', 'OFC_DIE_1', 'OFC_DIE_2', 'OFC_DIE_3',
    'OFC_PAIN_2', 'OFC_DIE_4', 'OFC_DEAD',
    'OFC_SHOOT1', 'OFC_SHOOT2', 'OFC_SHOOT3',
    # ghosts
    'BLINKY_W1', 'BLINKY_W2', 'PINKY_W1', 'PINKY_W2',
    'CLYDE_W1', 'CLYDE_W2', 'INKY_W1', 'INKY_W2',
    # hans
    'BOSS_W1', 'BOSS_W2', 'BOSS_W3', 'BOSS_W4',
    'BOSS_SHOOT1', 'BOSS_SHOOT2', 'BOSS_SHOOT3', 'BOSS_DEAD',
    'BOSS_DIE1', 'BOSS_DIE2', 'BOSS_DIE3',
    # schabbs
    'SCHABB_W1', 'SCHABB_W2', 'SCHABB_W3', 'SCHABB_W4',
    'SCHABB_SHOOT1', 'SCHABB_SHOOT2',
    'SCHABB_DIE1', 'SCHABB_DIE2', 'SCHABB_DIE3', 'SCHABB_DEAD',
    'HYPO1', 'HYPO2', 'HYPO3', 'HYPO4',
    # fake
    'FAKE_W1', 'FAKE_W2', 'FAKE_W3', 'FAKE_W4',
    'FAKE_SHOOT', 'FIRE1', 'FIRE2',
    'FAKE_DIE1', 'FAKE_DIE2', 'FAKE_DIE3', 'FAKE_DIE4',
    'FAKE_DIE5', 'FAKE_DEAD',
    # hitler
    'MECHA_W1', 'MECHA_W2', 'MECHA_W3', 'MECHA_W4',
    'MECHA_SHOOT1', 'MECHA_SHOOT2', 'MECHA_SHOOT3', 'MECHA_DEAD',
    'MECHA_DIE1', 'MECHA_DIE2', 'MECHA_DIE3',
    'HITLER_W1', 'HITLER_W2', 'HITLER_W3', 'HITLER_W4',
    'HITLER_SHOOT1', 'HITLER_SHOOT2', 'HITLER_SHOOT3', 'HITLER_DEAD',
    'HITLER_DIE1', 'HITLER_DIE2', 'HITLER_DIE3', 'HITLER_DIE4',
    'HITLER_DIE5', 'HITLER_DIE6', 'HITLER_DIE7',
    # giftmacher
    'GIFT_W1', 'GIFT_W2', 'GIFT_W3', 'GIFT_W4',
    'GIFT_SHOOT1', 'GIFT_SHOOT2',
    'GIFT_DIE1', 'GIFT_DIE2', 'GIFT_DIE3', 'GIFT_DEAD',
    # Rocket, smoke and small explosion
    'ROCKET_1', 'ROCKET_2', 'ROCKET_3', 'ROCKET_4',
    'ROCKET_5', 'ROCKET_6', 'ROCKET_7', 'ROCKET_8',
    'SMOKE_1', 'SMOKE_2', 'SMOKE_3', 'SMOKE_4',
    'BOOM_1', 'BOOM_2', 'BOOM_3',
    # gretel
    'GRETEL_W1', 'GRETEL_W2', 'GRETEL_W3', 'GRETEL_W4',
    'GRETEL_SHOOT1', 'GRETEL_SHOOT2', 'GRETEL_SHOOT3', 'GRETEL_DEAD',
    'GRETEL_DIE1', 'GRETEL_DIE2', 'GRETEL_DIE3',
    # fat face
    'FAT_W1', 'FAT_W2', 'FAT_W3', 'FAT_W4',
    'FAT_SHOOT1', 'FAT_SHOOT2', 'FAT_SHOOT3', 'FAT_SHOOT4',
    'FAT_DIE1', 'FAT_DIE2', 'FAT_DIE3', 'FAT_DEAD',
    # bj
    'BJ_W1, BJ_W2', 'BJ_W3', 'BJ_W4',
    'BJ_JUMP1', 'BJ_JUMP2', 'BJ_JUMP3', 'BJ_JUMP4',
    # player attack frames
    'KNIFEREADY', 'KNIFEATK1', 'KNIFEATK2', 'KNIFEATK3',
    'KNIFEATK4',
    'PISTOLREADY', 'PISTOLATK1', 'PISTOLATK2', 'PISTOLATK3',
    'PISTOLATK4',
    'MACHINEGUNREADY', 'MACHINEGUNATK1', 'MACHINEGUNATK2,MACHINEGUNATK3',
    'MACHINEGUNATK4',
    'CHAINREADY', 'CHAINATK1', 'CHAINATK2', 'CHAINATK3',
    'CHAINATK4'
])
