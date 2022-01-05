import os
import sqlite3

from JSON_to_DB import run_default

from Debug_engine import log_debug

class DB:
    def __init__(self, test_mode = False, db_path = 'tournament_stats.db', empty = False):
        if(test_mode):
            self.conn = sqlite3.connect(':memory:')
            self.create_tables()
            self.populate_default_vals()
            if not empty: self.populate_from_JSON()
        else:
            if(os.path.exists(db_path) == False):
                log_debug("No DB found, setting up a local DB")
                self.conn = sqlite3.connect(db_path)
                self.create_tables()
                self.populate_default_vals()
                if not empty: self.populate_from_JSON()
                log_debug("DB setup successfully, moving on")
            else:
                log_debug("DB exists already, proceeding..")
                self.conn = sqlite3.connect(db_path)
            
    def close_connecton(self):
        self.conn.close()

    def populate_from_JSON(self):
        run_default(self)

    def create_tables(self):
        with(self.conn):
            c = self.conn.cursor()
            # Enable foreign key support
            c.execute("PRAGMA foreign_keys = ON")
            # Players table
            c.execute("""CREATE TABLE players(
                    id integer primary key autoincrement,
                    first text NOT NULL,
                    last text NOT NULL,
                    Nr integer NOT NULL,
                    team integer NOT NULL,
                    role integer NOT NULL
                    )
            """)
            # Teams table
            c.execute("""CREATE TABLE teams(
                    id integer primary key autoincrement,
                    name text NOT NULL)
            """)
            # Roles table
            c.execute("""CREATE TABLE roles(
                    id integer primary key autoincrement,
                    name text NOT NULL)
            """)
            # Event classificator table
            c.execute("""CREATE TABLE event_class(
                    id integer primary key autoincrement,
                    name text NOT NULL)
            """)
            # Event classificator table
            c.execute("""CREATE TABLE refs(
                    id integer primary key autoincrement,
                    first text NOT NULL,
                    last text NOT NULL
                    )
            """)
            # Matches table
            c.execute("""CREATE TABLE match(
                    id integer primary key autoincrement,
                    main_ref integer NOT NULL,
                    ref_1 integer,
                    ref_2 integer,
                    fan_count integer,
                    team_A text NOT NULL,
                    team_B text NOT NULL,
                    location text NOT NULL,
                    date text NOT NULL,
                    FOREIGN KEY(ref_1) REFERENCES refs(id),
                    FOREIGN KEY(ref_2) REFERENCES refs(id),
                    FOREIGN KEY(main_ref) REFERENCES refs(id),
                    FOREIGN KEY(team_A) REFERENCES teams(id),
                    FOREIGN KEY(team_B) REFERENCES teams(id)
                    )
            """)
            # Signup for match table
            c.execute("""CREATE TABLE team_comp(
                    match integer NOT NULL,
                    team integer NOT NULL,
                    player integer,
                    FOREIGN KEY(match) REFERENCES match(id),
                    FOREIGN KEY(team) REFERENCES teams(id),
                    FOREIGN KEY(player) REFERENCES players(id)
                    )
            """)
            # Match start table
            c.execute("""CREATE TABLE field_players(
                    match integer NOT NULL,
                    team integer NOT NULL,
                    player integer NOT NULL,
                    FOREIGN KEY(match) REFERENCES match(id),
                    FOREIGN KEY(team) REFERENCES teams(id)
                    FOREIGN KEY(player) REFERENCES players(id)
                    )
            """)
            # Match events table
            c.execute("""CREATE TABLE events(
                    player integer NOT NULL,
                    event integer NOT NULL,
                    match integer NOT NULL,
                    time text,
                    FOREIGN KEY(player) REFERENCES players(id),
                    FOREIGN KEY(event) REFERENCES event_class(id),
                    FOREIGN KEY(match) REFERENCES match(id)
                    )
            """)

    def record_exists(self, table_name, values):
        with self.conn:
            c = self.conn.cursor()  
            table_details = c.execute("PRAGMA table_info({});".format(table_name)).fetchall()
            cols = []
            for column in table_details:
                if "id" not in column[1]:
                    cols.append(column[1])
            attr_string = ''
            for idx,i in enumerate(cols):
                if idx == 0:
                    if type(values[idx]) == int:
                        attr_string += '{} == {}'.format(i, values[idx])
                    elif type(values[idx]) == str:
                        attr_string += '{} == \'{}\''.format(i, values[idx])
                else:
                    if type(values[idx]) == int:
                        attr_string += '\nAND {} = {}'.format(i, values[idx])
                    elif type(values[idx]) == str:
                        attr_string += '\nAND {} = \'{}\''.format(i, values[idx])

            query = "SELECT * FROM {} WHERE {}".format(table_name,attr_string)
            log_debug(query)                  
            res = c.execute("SELECT * FROM {} WHERE {}".format(table_name,attr_string)).fetchone()
            if res != None: return True
            else: return False

    def populate_default_vals(self):
        # # Roles
        self.add_data("roles", ['V'])
        self.add_data("roles", ['U'])
        self.add_data("roles", ['A'])
        # Events
        self.add_data("event_class", ['Varti'])
        self.add_data("event_class", ['Piespele'])
        self.add_data("event_class", ['Dzeltena kartina'])
        self.add_data("event_class", ['Maina prom'])
        self.add_data("event_class", ['Maina uz'])
        self.add_data("event_class", ['Soda sitiens'])
        self.add_data("event_class", ['Sarkana kartina'])

    def get_ref_ID(self, first, last):
        c = self.conn.cursor()
        query = """SELECT id from refs 
                            WHERE first = '{}'
                              AND last = '{}'
                        """.format(first, last)
        log_debug(query)
        res = c.execute(query).fetchone()
        return res
    
    def get_player_ID(self, Nr, team):
        c = self.conn.cursor()
        query = """SELECT players.id
                    FROM players
                    LEFT JOIN teams
                    ON teams.id = {}
                    WHERE players.team = teams.id
                    AND players.Nr = {}
                    """.format(team, Nr)
        
        log_debug(query)
        res = c.execute(query).fetchone()
        return res

    def get_role_ID(self, role):
        c = self.conn.cursor()
        query = """SELECT id from roles 
                    WHERE name = '{}'
                    """.format(role)
        log_debug(query)
        res = c.execute(query).fetchone()
        return res

    def get_team_id(self, team_name):
        c = self.conn.cursor()
        query = """SELECT id from teams 
                    WHERE name = '{}'
                    """.format(team_name)
        log_debug(query)
        res = c.execute(query).fetchone()
        return res

    def get_event_id(self, event_name):
        c = self.conn.cursor()
        query = """SELECT id from event_class 
                    WHERE name = '{}'
                    """.format(event_name)
        log_debug(query)
        res = c.execute(query).fetchone()
        return res

    def add_data(self, table_name, values):
        with self.conn:
            c = self.conn.cursor()  
            
            table_details = c.execute("PRAGMA table_info({});".format(table_name)).fetchall()
            cols = []
            for column in table_details:
                if "id" not in column[1]:
                    cols.append(column[1])

            vals = ()
            for value in values:
                vals += (value,)

            col_string = ''
            val_string = ''
            for idx, item in enumerate(cols):
                if idx != (len(cols) -1):
                    if type(item) == str:
                        col_string += item + ", "
                    else: 
                        col_string += str(item) + ", " 
                    val_string += '?, '
                else: 
                    if type(item) == str:
                        col_string += item 
                    else:
                        col_string += str(item)
                    val_string += '?'
            # print("INSERT INTO {} ({}) VALUES ({})".format(table_name, col_string, val_string), vals)
            log_debug("INSERT INTO {} ({}) VALUES ({})".format(table_name, cols, values))                    
            c.execute("INSERT INTO {} ({}) VALUES ({})".format(table_name, col_string,val_string),vals)

    def get_match_id(self, team_A, team_B, location, date):
        c = self.conn.cursor()
        query = """SELECT id from match 
                    WHERE team_A = '{}'
                    AND team_B = '{}'
                    AND location = '{}'
                    AND date = '{}'
                    """.format(team_A, team_B, location, date)
        log_debug(query)
        res = c.execute(query).fetchone()
        return res

    def get_dropdown_data(self):
        c = self.conn.cursor()
        query = """SELECT t1.name, t2.name 
                   FROM match m
                   LEFT JOIN teams t1
                   ON m.team_A = t1.id
                   LEFT JOIN teams t2
                   ON m.team_B = t2.id
                   ORDER BY m.id
                   """
        log_debug(query)
        teams = c.execute(query).fetchall()

        query = """SELECT p.first, p.last, p.Nr, t.name
                   FROM players p
                   LEFT JOIN team_comp tc
                   ON tc.player = p.id
                   LEFT JOIN teams t
                   ON t.id = tc.team
                   GROUP BY p.first, p.last, t.name
                   """

        log_debug(query)
        players = c.execute(query).fetchall()

        return teams, players

    def get_tournament_data(self):
        c = self.conn.cursor()
        tournament_points = []
        match_count = c.execute("SELECT count(id) from match").fetchall()[0][0]
        for match in range(match_count):
            ot_win = False
            match_dict = {}

            query = """SELECT t.name, e.time, t.name, e.match
                    FROM events e
                    LEFT JOIN players p
                    ON p.id = e.player
                    LEFT JOIN event_class ec
                    ON e.event = ec.id
                    LEFT JOIN teams t
                    ON p.team = t.id
                    WHERE e.match = {}
                    AND (ec.name = 'Varti' OR ec.name = 'Soda sitiens')
                    ORDER BY e.match
                    """.format(match+1)
            log_debug(query)
            match_goals = c.execute(query).fetchall()
            teams = c.execute("""SELECT t1.name, t2.name 
                                    FROM match m
                                    LEFT JOIN teams t1
                                    ON m.team_A = t1.id
                                    LEFT JOIN teams t2
                                    ON m.team_B = t2.id
                                    WHERE m.id = {}
                                    """.format(match_goals[0][3])).fetchall()[0]
            log_debug(query)
            match_goals = c.execute(query).fetchall()

            for team in teams: match_dict[team] = 0
            for goal in match_goals:
                if goal[0] in match_dict.keys():
                    match_dict[goal[0]] += 1
                else: match_dict[goal[0]] = 1
                if (int(goal[1][:2]) >= 60): ot_win = True
            
            tournament_points.append([match_dict, ot_win])

        return tournament_points

    def get_players_data(self):
        c = self.conn.cursor()
        
        query = """SELECT ec.name, e.match, p.team, p.id, p.first, p.last, t.name
                    FROM events e
                    LEFT JOIN players p
                    ON e.player = p.id
                    LEFT JOIN event_class ec
                    ON e.event = ec.id
                    LEFT JOIN teams t
                    ON p.team = t.id
                    WHERE (ec.name = 'Varti'
                        OR ec.name = 'Soda sitiens'
                        OR ec.name = 'Piespele')
                    ORDER BY e.match
                    """
        log_debug(query)
        match_events = c.execute(query).fetchall()

        query_all = """SELECT p.id, p.first, p.last, t.name
                    FROM players p
                    LEFT JOIN teams t
                    ON p.team = t.id
                    """
        log_debug(query)

        player_achievements = {}

        for p in c.execute(query_all).fetchall():
            player_achievements[p[0]] = [0,0,0,p[1],p[2],p[3]]

        for e in match_events:
            if e[0] == 'Varti':
                player_achievements[e[3]][0] += 1
            if e[0] == 'Piespele':
                player_achievements[e[3]][1] += 1
            if e[0] == 'Soda sitiens':
                player_achievements[e[3]][2] += 1

        return player_achievements

    def get_player_data(self, Nr, team):
        c = self.conn.cursor()
        query = """SELECT ec.name, e.time, (SELECT t1.name || '-' || t2.name
                                                    FROM match m
                                                    LEFT JOIN teams t1
                                                    ON m.team_A = t1.id
                                                    LEFT JOIN teams t2
                                                    ON m.team_B = t2.id
                                                    WHERE m.id = e.match)
                    FROM events e
                    LEFT JOIN event_class ec
                    ON ec.id = e.event
                    LEFT JOIN players p
                    ON e.player = p.id
                    LEFT JOIN teams t
                    ON p.team = t.id
                    WHERE p.Nr = '{}'
                    AND t.name = '{}'
                    GROUP BY ec.name, t.name, e.time
                    ORDER BY e.match ASC, e.time ASC
                    """.format(Nr, team)

        log_debug(query)
        player_events = c.execute(query).fetchall()
        return player_events

    def get_game_data(self, team_A, team_B):
        c = self.conn.cursor()
        query = """SELECT (SELECT p.first || ' ' || p.last
                            FROM players p
                            WHERE e.player = p.id)
                    ,p.Nr
                    ,e.time
                    ,ec.name
                    FROM events e
                    LEFT JOIN match m
                    ON m.id = e.match
                    LEFT JOIN players p
                    ON p.id = e.player
                    LEFT JOIN teams t1
                    ON t1.name = '{}'
                    LEFT JOIN teams t2
                    ON t2.name = '{}'
                    LEFT JOIN event_class ec
                    ON ec.id = e.event
                    WHERE m.team_A = t1.id 
                    AND m.team_B = t2.id
                    ORDER BY e.time
                    """.format(team_A, team_B)

        log_debug(query)
        game_events = c.execute(query).fetchall()
        return game_events

