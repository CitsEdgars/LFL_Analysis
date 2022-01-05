from os import listdir
from os.path import isfile, join
import pathlib
import json
from types import SimpleNamespace

def store_player(db, first, last, player_Nr, team_name, role):
    team = db.get_team_id(team_name)[0]
    exists = db.get_player_ID(player_Nr,team) != None
    if not exists:
        db.add_data("players",[first,last,player_Nr,team,role])

def store_ref(db, first, last):
    exists = db.get_ref_ID(first,last) != None
    if not exists:
        db.add_data("refs",[first,last])

def store_team(db, team_name):
    exists = db.get_team_id(team_name) != None
    if not exists:
        db.add_data("teams",[team_name])

def store_team_players(db, team_name, match_id, Nr):
    team_id = db.get_team_id(team_name)[0]
    player_id = db.get_player_ID(Nr,team_id)[0]
    if not db.record_exists("team_comp",[match_id, team_id, player_id]):
        db.add_data("team_comp",[match_id, team_id, player_id])

def store_field_players(db, team_name, match_id, Nr):
    team_id = db.get_team_id(team_name)[0]
    player_id = db.get_player_ID(Nr,team_id)[0]
    if not db.record_exists("field_players",[match_id, team_id, player_id]):
        db.add_data("field_players",[match_id, team_id, player_id])

def store_match(db, main_ref, refs, location, time, fans, team_A, team_B):
    main_ref_id = db.get_ref_ID(main_ref[0],main_ref[1])[0]
    ref_1_id = db.get_ref_ID(refs[0][0],refs[0][1])[0]
    ref_2_id = db.get_ref_ID(refs[1][0],refs[1][1])[0]
    team_A_id = db.get_team_id(team_A)[0]
    team_B_id = db.get_team_id(team_B)[0]
    if not db.record_exists("match",[main_ref_id, ref_1_id, ref_2_id, fans, team_A_id, team_B_id, location, time]):
        db.add_data("match",[main_ref_id, ref_1_id, ref_2_id, fans, team_A_id, team_B_id, location, time])
        match_id = db.get_match_id(team_A_id, team_B_id, location, time)[0]
        return match_id

def store_event(db, player_Nr, event_name, match_id, team_name, time):
    event_id = db.get_event_id(event_name)[0]
    team_id = db.get_team_id(team_name)[0]
    player_id = db.get_player_ID(player_Nr,team_id)[0]
    if not db.record_exists("events", [player_id, event_id, match_id, time]):
        db.add_data("events", [player_id, event_id, match_id, time])

def run_default(db, folders = ["\\data\\1", "\\data\\2"]):
    mypath = pathlib.Path().resolve()
    for folder in folders:
        path = str(mypath)+folder
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        for file in onlyfiles:
            filename = folder[1:] + "\\" + file
            JSON_to_DB(db, filename)

def JSON_to_DB(db, filename):
    f = open(filename)
    data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    f.close()
    speles_info = data.Spele

    # Refs 
    main_ref = [speles_info.VT.Vards, speles_info.VT.Uzvards]
    store_ref(db, main_ref[0], main_ref[1])
    basic_refs = []
    for ref in speles_info.T:
        basic_refs.append([ref.Vards, ref.Uzvards])
        store_ref(db, ref.Vards, ref.Uzvards)
    
    # Teams and players
    for team in speles_info.Komanda:
        store_team(db, team.Nosaukums)
        for player in team.Speletaji.Speletajs:
            store_player(db, player.Vards, player.Uzvards, player.Nr, team.Nosaukums, player.Loma)
    
    # Match info
    main_ref = [speles_info.VT.Vards, speles_info.VT.Uzvards]
    location = speles_info.Vieta
    time = speles_info.Laiks
    fans = speles_info.Skatitaji
    team_A = speles_info.Komanda[0].Nosaukums
    team_B = speles_info.Komanda[1].Nosaukums
    match_id = store_match(db, main_ref, basic_refs, location, time, fans, team_A, team_B)
    if match_id == None: return
        
    for team in speles_info.Komanda: 
        #Team composition for the match
        for player in team.Speletaji.Speletajs:
            store_team_players(db, team.Nosaukums, match_id, player.Nr)
        for player in team.Pamatsastavs.Speletajs:
            store_field_players(db, team.Nosaukums, match_id, player.Nr)

        if hasattr(team.Varti, "VG"):
            if type(team.Varti.VG) != list:
                goal = team.Varti.VG
                if (team.Varti.VG.Sitiens != 'J'):
                    store_event(db, goal.Nr, 'Varti', match_id, team.Nosaukums, goal.Laiks)
                else: 
                    store_event(db, goal.Nr, 'Soda sitiens', match_id, team.Nosaukums, goal.Laiks)
                if hasattr(goal, "P"):
                    if type(goal.P) != list: 
                        store_event(db, goal.P.Nr, 'Piespele', match_id, team.Nosaukums, goal.Laiks)
                    else: 
                        for pas in goal.P:
                            store_event(db, pas.Nr, 'Piespele', match_id, team.Nosaukums, goal.Laiks)
            else:
                for goal in team.Varti.VG:
                    if (goal.Sitiens != 'J'):
                        store_event(db, goal.Nr, 'Varti', match_id, team.Nosaukums, goal.Laiks)
                    else: 
                        store_event(db, goal.Nr, 'Soda sitiens', match_id, team.Nosaukums, goal.Laiks)
                    if hasattr(goal, "P"):
                        if type(goal.P) != list: 
                            store_event(db, goal.P.Nr, 'Piespele', match_id, team.Nosaukums, goal.Laiks)
                        else: 
                            for pas in goal.P:
                                store_event(db, pas.Nr, 'Piespele', match_id, team.Nosaukums, goal.Laiks)

        if hasattr(team.Mainas, "Maina"):
            if type(team.Mainas.Maina) != list: 
                change = team.Mainas.Maina
                store_event(db, change.Nr1, 'Maina prom', match_id, team.Nosaukums, change.Laiks)
                store_event(db, change.Nr2, 'Maina uz', match_id, team.Nosaukums, change.Laiks)
            else: 
                for change in team.Mainas.Maina:
                    store_event(db, change.Nr1, 'Maina prom', match_id, team.Nosaukums, change.Laiks)
                    store_event(db, change.Nr2, 'Maina uz', match_id, team.Nosaukums, change.Laiks)
        
        if hasattr(team.Sodi, "Sods"):
            if type(team.Sodi.Sods) != list: 
                pun = team.Sodi.Sods
                store_event(db, pun.Nr, 'Dzeltena kartina', match_id, team.Nosaukums, pun.Laiks)
            else: 
                players_warned = []
                for pun in team.Sodi.Sods:
                    if [pun.Nr,team.Nosaukums] in players_warned:

                        store_event(db, pun.Nr, 'Sarkana kartina', match_id, team.Nosaukums, pun.Laiks)
                    else:
                        players_warned.append([pun.Nr,team.Nosaukums])
                        store_event(db, pun.Nr, 'Dzeltena kartina', match_id, team.Nosaukums, pun.Laiks)

