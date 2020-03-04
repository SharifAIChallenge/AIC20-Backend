from apps.challenge.models import GameTeam, GameSide


def update_game_team_scoreboard_score(game, scoreboard):
    client0 = game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[0]
    client1 = game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[0]
    client2 = game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[1]
    client3 = game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[1]
    if client0.score and client1.score and client2.score and client3.score:
        row0 = scoreboard.rows.get(team=client0.team)
        row1 = scoreboard.rows.get(team=client1.team)
        row2 = scoreboard.rows.get(team=client2.team)
        row3 = scoreboard.rows.get(team=client3.team)
        S1 = row0.score + row2.score
        S2 = row1.score + row3.score
        R1 = client0.score + client2.score
        R2 = client1.score + client3.score
        P1 = (1.0 / (1.0 + 10 ** ((S2 - S1) / 400)))
        P2 = (1.0 / (1.0 + 10 ** ((S1 - S2) / 400)))
        game_side1 = GameTeam.objects.filter(team=client0.team).get(game_side__game=game).game_side
        game_side2 = GameTeam.objects.filter(team=client1.team).get(game_side__game=game).game_side
        if game_side1.has_won:
            actual_score1, actual_score2 = 1, 0
        elif not game_side1.has_won and not game_side2.has_won:
            actual_score1, actual_score2 = 0.5, 0.5
        else:
            actual_score1, actual_score2 = 0, 1
        added_score1 = 30 * (actual_score1 - P1)
        added_score2 = 30 * (actual_score2 - P2)
        if added_score1 > 0:
            client0.scoreboard_score = added_score1 * (client0.score / R1)
            client2.scoreboard_score = added_score1 * (client2.score / R1)
        else:
            client0.scoreboard_score = added_score1 * (client2.score / R1)
            client2.scoreboard_score = added_score1 * (client0.score / R1)
        if added_score2 > 0:
            client1.scoreboard_score = added_score2 * (client1.score / R2)
            client3.scoreboard_score = added_score2 * (client3.score / R2)
        else:
            client1.scoreboard_score = added_score2 * (client3.score / R2)
            client3.scoreboard_score = added_score2 * (client1.score / R2)
        client0.save()
        client1.save()
        client2.save()
        client3.save()
        row0.score += client0.scoreboard_score
        row1.score += client1.scoreboard_score
        row2.score += client2.scoreboard_score
        row3.score += client3.scoreboard_score
        row0.save()
        row1.save()
        row2.save()
        row3.save()
