class InterpolationParams:
    SMOOTHNESS_MIN = 5
    SMOOTHNESS_MAX = SMOOTHNESS_MIN + 15
    SMOOTHNESS_DEFAULT = SMOOTHNESS_MIN + (SMOOTHNESS_MAX - SMOOTHNESS_MIN) / 2
    SMOOTHNESS_DEVIDER = 100

    # Расстояние, после которого перестаёт учитываться угол движения при интерполяции
    INTERPOLATION_THRESHOLD = 50
    INTERPOLATION_ANGLE_SCALE = 0.2


class Ui:
    SMOOTHNESS_MIN = InterpolationParams.SMOOTHNESS_MIN
    SMOOTHNESS_MAX = InterpolationParams.SMOOTHNESS_MAX
    SMOOTHNESS_DEFAULT = InterpolationParams.SMOOTHNESS_DEFAULT
    
    SCALE_MIN = 5
    SCALE_MAX = 100


class Methods:
    MOVIE_GET = 100
    MOVIE_SET = 101

    SCALE_GET = 102
    SCALE_SET = 103

    SMOOTH_GET = 104
    SMOOTH_SET = 105

    TARGET_GET = 106
    CURRENT_GET = 107
    PREVIOUS_GET = 108


class Variables:
    ANIMATED_MOVEMENT = 200 # BOOL


class ConfigKeys:
    PATH = 'startup.path'
    SCALE = 'startup.scale'
    SMOOTH = 'startup.smooth'
    UPDATE_OVERLAY_DELAY = 'overlay.update_delay'
    ANIMATED_MOVEMENT = 'startup.animated_movement'
    

class ConfigDefaults:
    PATH = ''
    SCALE = 50
    SMOOTH = InterpolationParams.SMOOTHNESS_DEFAULT
    UPDATE_OVERLAY_DELAY = 15
    ANIMATED_MOVEMENT = False