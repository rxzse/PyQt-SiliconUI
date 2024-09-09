from siui.core.animation.abstract import ABCSiAnimation


class SiAnimationGroup:
    """
    Animation groups provide support for managing multiple animations and allow access to animation objects using tokens
    """
    def __init__(self):
        self.animations = []
        self.tokens = []

    def addMember(self, ani, token: str):
        if token in self.tokens:
            raise ValueError(f"Code already exists: {token}")
        self.animations.append(ani)
        self.tokens.append(token)

    def fromToken(self, aim_token: str) -> ABCSiAnimation:
        for ani, token in zip(self.animations, self.tokens):
            if token == aim_token:
                return ani
        raise ValueError(f"The passed in token was not found in the token group: {aim_token}")
