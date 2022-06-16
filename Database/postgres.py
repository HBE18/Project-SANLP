import psycopg2

class Postgres():
    def __init__(self) -> None:
        db = psycopg2.connect(user = "postgres",
                      password = "123456",
                      host = "25.33.228.221",
                      port = "5432",
                      database = "sanlp")
        
        self.cursor = db.cursor()

    def getAllKeywords(self) -> list[str]:
        query = "SELECT keyword FROM keywords;"

        self.cursor.execute(query)

        res = self.cursor.fetchall()

        result = []

        for i in res:
            result.append(i[0])
        
        return result
    
    def getUserIdListOfTheKeyword(self,keyword:str) -> list[int]:
        query = f"SELECT ids FROM keywords WHERE keyword='{keyword}'"

        self.cursor.execute(query)

        res = self.cursor.fetchall()

        return res[0][0]