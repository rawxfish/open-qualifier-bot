import common
from tokens import *
from watchlist import NOTABLE_BY_REGION



def _is_notable(game):
    def _is_notable_team(team):
        return team["team_id"] in NOTABLE_BY_REGION["China"]

    if "dire_team" in game and _is_notable_team(game["dire_team"]):
        return True
    if "radiant_team" in game and _is_notable_team(game["radiant_team"]):
        return True
    return False


def get_matches():
    uri = "https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/?key=%s" % (STEAM_KEY)
    result = common.get_json(uri)
    if result is None or "result" not in result:
        return "No notable teams detected in live matches.\n\n"

    match_str = ""
    for game in result["result"]["games"]:
        if int(game["league_id"]) == LEAGUE_ID and _is_notable(game):
            dire = game.get("dire_team", {}).get("team_name", "Dire")
            radiant = game.get("radiant_team", {}).get("team_name", "Radiant")
            match_str += "[**%s**](http://www.trackdota.com/matches/%s) \n\n" % ("%s vs. %s" % (dire, radiant), game["match_id"])

    if len(match_str) == 0:
        match_str = "No notable teams detected in live matches."

    return match_str

