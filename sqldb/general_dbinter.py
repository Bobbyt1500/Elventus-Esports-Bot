import sqlite3

class DBInterface:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
    
    def replace_role_assign_ids(self, role_assign_ids):
        # Delete old ids
        cur = self.conn.cursor()
        cur.execute('''DELETE FROM role_assign_ids''')

        # Add new ones
        sql_statement = ''' INSERT INTO role_assign_ids(id)
                            VALUES(?) '''
        for role_assign_id in role_assign_ids:
            self.conn.execute(sql_statement, (role_assign_id,))

        self.conn.commit()
    
    def is_role_assign_id(self, given_id):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM role_assign_ids WHERE id = ?''', (given_id,))
        data = cur.fetchall()

        if len(data) == 0:
            return False
        else:
            return True
        
