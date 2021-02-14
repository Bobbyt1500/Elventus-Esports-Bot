import sqlite3
import scrim_scheduler.scrim_scheduler_config

class DBInterface:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
    
    def get_scheduled_matches(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM scheduled_matches''')
        return cur.fetchall()
    
    def get_scheduled_matches_for_team(self, team):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM scheduled_matches WHERE team1 = ? OR team2 = ?''',(team, team))
        return cur.fetchall()
    
    def get_invite_from_code(self, code):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM invite_codes WHERE code = ?''', (code,))
        data = cur.fetchall()

        if len(data) == 0:
            return None
        else:
            return data[0]

    def get_invite_code(self, team, day, time):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM invite_codes WHERE team = ? AND day = ? AND time = ?''', (team, day, time))
        return cur.fetchall()[0][0]
    
    def get_ALL_invites_sent_by_team(self, team):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM invites WHERE sending_team = ?''', (team, ))
        return cur.fetchall()

    def get_invites_sent_by_team(self, team, day, time):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM invites WHERE sending_team = ? AND day = ? AND time = ?''', (team, day, time))
        return cur.fetchall()
    
    def get_recieved_invite_at_time(self, team, day, time):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM invites WHERE recieving_team = ? AND day = ? AND time = ?''', (team, day, time))
        data = cur.fetchall()

        if len(data) == 0:
            return None
        else:
            return data[0]
        
    def get_recieved_invites_at_time(self, team, day, time):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM invites WHERE recieving_team = ? AND day = ? AND time = ?''', (team, day, time))
        data = cur.fetchall()

        if len(data) == 0:
            return None
        else:
            return data
    
    def get_recieved_invites(self, team):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM invites WHERE recieving_team = ?''',(team,))
        return cur.fetchall()
    
    def get_blocked_slots(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM blocked_slots''')
        return cur.fetchall()

    def get_teams_blocked_slots(self, team):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM blocked_slots WHERE team = ?''', (team, ))
        return cur.fetchall()

    def replace_team_agenda(self, team, id):
        #Remove old team agenda
        cur = self.conn.cursor()
        cur.execute('''DELETE FROM team_agendas WHERE team = ?''', (team,))
        sql_statement = ''' INSERT INTO team_agendas(team, id)
                            VALUES(?,?) '''
        self.conn.execute(sql_statement, (team ,id))
        self.conn.commit()
    
    def delete_blocked_slot(self, team, day, time):
        cur = self.conn.cursor()
        cur.execute('''DELETE FROM blocked_slots WHERE team = ? AND day = ? AND time = ?''', (team, day, time))
        self.conn.commit()
    
    def delete_all_invite_codes(self):
        cur = self.conn.cursor()
        cur.execute('''DELETE FROM invite_codes''')
        self.conn.commit()
    
    def delete_all_scheduled_matches(self):
        cur = self.conn.cursor()
        cur.execute('''DELETE FROM scheduled_matches''')
        self.conn.commit()

    def delete_all_invites(self):
        cur = self.conn.cursor()
        cur.execute('''DELETE FROM invites''')
        self.conn.commit()

    def delete_all_blocked_slots(self):
        cur = self.conn.cursor()
        cur.execute('''DELETE FROM blocked_slots''')
        self.conn.commit()
    
    def delete_teams_invite_codes(self, team):
        cur = self.conn.cursor()
        cur.execute(''' DELETE FROM invite_codes WHERE team = ?''', (team, ))

    def delete_teams_blocked_slots(self, team_name):
        cur = self.conn.cursor()
        cur.execute(''' DELETE FROM blocked_slots WHERE team = ?''', (team_name, ))
        self.conn.commit()
    
    def delete_invites_involving_team(self, team):
        cur = self.conn.cursor()
        cur.execute(''' DELETE FROM invites WHERE sending_team = ? OR recieving_team = ?''', (team, team))
        self.conn.commit()
    
    def delete_scheduled_matches_involving_team(self, team):
        cur = self.conn.cursor()
        cur.execute(''' DELETE FROM scheduled_matches WHERE team1 = ? OR team2 = ? ''', (team, team))

    def delete_invites_sent_from_team(self, sending_team, day, time):
        cur = self.conn.cursor()
        cur.execute(''' DELETE FROM invites WHERE sending_team = ? AND day = ? AND time = ?''', (sending_team, day, time))
        self.conn.commit()
    
    def delete_team_agenda_id(self, team):
        cur = self.conn.cursor()
        cur.execute(''' DELETE FROM team_agendas WHERE team = ?''', (team, ))
        self.conn.commit()
    
    def delete_scheduled_match(self, team1, team2, day, time):
        cur = self.conn.cursor()
        # Team 1 or team 2 could be flipped
        cur.execute('''DELETE FROM scheduled_matches WHERE team1 = ? AND team2 = ? AND day = ? AND time = ?''',(team1, team2, day, time))
        cur.execute('''DELETE FROM scheduled_matches WHERE team1 = ? AND team2 = ? AND day = ? AND time = ?''',(team2, team1, day, time))
        self.conn.commit()
    
    def insert_blocked_slot(self, team, day, time):
        sql_statement = ''' INSERT INTO blocked_slots(team, day, time)
                            VALUES(?,?,?) '''
        self.conn.execute(sql_statement, (team, day, time))
        self.conn.commit()

    def insert_scheduled_match(self, team1, team2, day, time):
        sql_statement = ''' INSERT INTO scheduled_matches(team1, team2, day, time)
                            VALUES(?,?,?,?) '''
        self.conn.execute(sql_statement, (team1, team2, day, time))
        self.conn.commit()

    def insert_invite_code(self, code, team, day, time):
        sql_statement = ''' INSERT INTO invite_codes(code, team, day, time)
                            VALUES(?,?,?,?) '''
        self.conn.execute(sql_statement, (code, team, day, time))
        self.conn.commit()
    
    def insert_invite(self, recieving_team, sending_team, day, time):
        sql_statement = ''' INSERT INTO invites(recieving_team, sending_team, day, time)
                            VALUES(?,?,?,?) '''
        self.conn.execute(sql_statement, (recieving_team, sending_team, day, time))
        self.conn.commit()