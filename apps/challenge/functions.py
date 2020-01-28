from .models import Game, Info

def run_single_match(match):
    info = Info(status = "pending", detail = "")
    info.save()
    game = Game(match = match, info = info)
    game.save()
    #TODO: send request to infra here
    return game
