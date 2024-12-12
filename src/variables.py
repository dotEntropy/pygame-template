from pygame.math import Vector2


class GameVars:
    # display
    client_w = None
    client_h = None
    fps = 240
    sprite_scale = 1

    # states
    states = {}
    active_state = None

    @staticmethod
    def get_center_pos() -> Vector2:
        return Vector2(GameVars.client_w, GameVars.client_h) // 2
