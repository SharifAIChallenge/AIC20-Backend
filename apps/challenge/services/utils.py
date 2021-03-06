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
        game_side1 = GameTeam.objects.filter(team=client0.team).filter(game_side__game=game).last().game_side
        game_side2 = GameTeam.objects.filter(team=client1.team).filter(game_side__game=game).last().game_side
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


def update_game_team_scoreboard_score_using_match(match, scoreboard):
    team_scores = {}

    got_team_scores = False

    for game in match.games.all():
        client0 = game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[0]
        client1 = game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[0]
        client2 = game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[1]
        client3 = game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[1]

        if not got_team_scores:
            row0 = scoreboard.rows.get(team=client0.team)
            row1 = scoreboard.rows.get(team=client1.team)
            row2 = scoreboard.rows.get(team=client2.team)
            row3 = scoreboard.rows.get(team=client3.team)

            team_scores[client0.team.name] = {'score': row0.score, 'row': row0}
            team_scores[client1.team.name] = {'score': row1.score, 'row': row1}
            team_scores[client2.team.name] = {'score': row2.score, 'row': row2}
            team_scores[client3.team.name] = {'score': row3.score, 'row': row3}
            got_team_scores = True

        if client0.score and client1.score and client2.score and client3.score:
            S1 = team_scores[client0.team.name]['score'] + team_scores[client2.team.name]['score']
            S2 = team_scores[client1.team.name]['score'] + team_scores[client3.team.name]['score']
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
            match_team0 = match.match_teams.get(team=client0.team)
            match_team1 = match.match_teams.get(team=client1.team)
            match_team2 = match.match_teams.get(team=client2.team)
            match_team3 = match.match_teams.get(team=client3.team)
            match_team0.score += client0.scoreboard_score
            match_team1.score += client1.scoreboard_score
            match_team2.score += client2.scoreboard_score
            match_team3.score += client3.scoreboard_score
            match_team0.save()
            match_team1.save()
            match_team2.save()
            match_team3.save()
            team_scores[client0.team.name]['row'].score += client0.scoreboard_score
            team_scores[client1.team.name]['row'].score += client1.scoreboard_score
            team_scores[client2.team.name]['row'].score += client2.scoreboard_score
            team_scores[client3.team.name]['row'].score += client3.scoreboard_score
            team_scores[client0.team.name]['row'].save()
            team_scores[client1.team.name]['row'].save()
            team_scores[client2.team.name]['row'].save()
            team_scores[client3.team.name]['row'].save()


def update_league_scoreboard(match, scoreboard):
    team_scores = {}
    got_team_scores = False

    for game in match.games.all():
        client0 = game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[0]
        client1 = game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[0]
        client2 = game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[1]
        client3 = game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[1]

        if not got_team_scores:
            row0 = scoreboard.rows.get(team=client0.team)
            row1 = scoreboard.rows.get(team=client1.team)
            row2 = scoreboard.rows.get(team=client2.team)
            row3 = scoreboard.rows.get(team=client3.team)

            team_scores[client0.team.name] = {'score': row0.score, 'row': row0}
            team_scores[client1.team.name] = {'score': row1.score, 'row': row1}
            team_scores[client2.team.name] = {'score': row2.score, 'row': row2}
            team_scores[client3.team.name] = {'score': row3.score, 'row': row3}
            got_team_scores = True

        if client0.score and client1.score and client2.score and client3.score:
            client0.scoreboard_score += client0.score
            client2.scoreboard_score += client2.score
            client1.scoreboard_score += client1.score
            client3.scoreboard_score += client3.score
            client0.save()
            client1.save()
            client2.save()
            client3.save()
            match_team0 = match.match_teams.get(team=client0.team)
            match_team1 = match.match_teams.get(team=client1.team)
            match_team2 = match.match_teams.get(team=client2.team)
            match_team3 = match.match_teams.get(team=client3.team)
            match_team0.score += client0.scoreboard_score
            match_team1.score += client1.scoreboard_score
            match_team2.score += client2.scoreboard_score
            match_team3.score += client3.scoreboard_score
            match_team0.save()
            match_team1.save()
            match_team2.save()
            match_team3.save()
            team_scores[client0.team.name]['row'].score += client0.score
            team_scores[client1.team.name]['row'].score += client1.score
            team_scores[client2.team.name]['row'].score += client2.score
            team_scores[client3.team.name]['row'].score += client3.score
            team_scores[client0.team.name]['row'].save()
            team_scores[client1.team.name]['row'].save()
            team_scores[client2.team.name]['row'].save()
            team_scores[client3.team.name]['row'].save()
