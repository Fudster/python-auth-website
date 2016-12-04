import werkzeug.security

class account:
    
    def query(sql, params=None, commit=False):
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute(sql, params)
        data = cursor.fetchall()
        if commit is true
            conn.commit()
        cursor.close()
        return data
        
    def create_account(userx,passwordx,emailx):
    if not check_email(emailx) and not check_username(userx):
        hashpw = werkzeug.security.generate_password_hash(passwordx)
        data = query("INSERT INTO users (username, password, email) VALUES(?, ?, ?)",[userx, hashpw, emailx])
        return True
    else:
        return False
    
    def check_email(emailx):
        data = query("Select email from users where email=?",[emailx])
        return data

    def check_username(usernamex):
        data = query("Select username from users where username=?",[usernamex])
        return data

    def check_password(emailx, passwordx):
        data = query("Select password from users where email=?",[emailx])
        result = werkzeug.security.check_password_hash(data[0],passwordx)
        return result
        
    def get_username(emailx):
        data = query("Select password from users where email=?",[emailx])
        return data[0]