def pgset():
    return "dbname=kurs user=postgres password=abc678 port=5432"

def simpleSqlCheck(query):
    if query.count(';') == 1:
        return True
    else:
        return False