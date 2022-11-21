import mysql.connector
from typing import Union
import os
import pandas as pd

class Converter:
    def __init__(self, host: str, user: str, password: str, 
                 excels: Union[list, str], database_name: str) -> None:
        self.user = user
        self.host = host
        self.password = password
        self.excels = excels
        self.database_name = database_name
        self.check_excels()
        self.connection = self.create_connection()
        self.cursor = self.connection.cursor()
        self.tables = []
        
    def create_connection(self):
        try: 
            connection = mysql.connector.connect(
                host=self.host,
                password=self.password,
                user=self.user,
                port=3306
            )
            return connection
        except mysql.connector.Error as err:
            print(err)
        
    def create_database(self) -> None:
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
        self.connection.commit()
        print(f"Database {self.database_name} created successfully")
    
    def create_tables(self, excel, headlines):
        excel = excel.replace(".xlsx", "")
        excel = excel.replace(".xls", "")
        excel = excel.replace(".xlsm", "")
        excel = excel.replace("-", "_")
        excel = excel.replace(" ", "_")
        excel = excel.replace(":", "")
        sql = f"""
        CREATE TABLE IF NOT EXISTS {excel} (
            id INT AUTO_INCREMENT PRIMARY KEY,
        """
        for headline in headlines:
            headline = headline.replace(" ", "_")
            headline = headline.replace("-", "_")
            headline = headline.replace(":", "")
            sql += f"{headline} LONGTEXT,"
        sql = sql[:-1] + ")"
        self.cursor.execute(sql)
        self.connection.commit()
        self.tables.append(excel)
        print(f"Table {excel} created successfully")
    
    def check_excels(self):
        if type(self.excels) == str:
            self.excels = [self.excels]
        for excel in self.excels:
            if not os.path.exists(f"excels/{excel}"):
                raise FileNotFoundError(f"File {excel} not found")
    
    def insert_data(self, excel, headlines, values):
        excel = excel.replace(".xlsx", "")
        sql = f"""insert into {excel} ("""
        for headline in headlines:
            sql += f"{headline},"
        sql = sql[:-1] + ") values ("
        for value in values:
            sql += f"'{value}',"
        sql = sql[:-1] + ")"
        sql = sql.replace(":", "")
        self.cursor.execute(sql)
        self.connection.commit()
        
    def convert_excels_to_sql(self):
        self.create_database()
        self.cursor.execute(f"USE {self.database_name}")
        for i, excel in enumerate(self.excels):
            self.create_tables(excel, self.get_headlines()[i])
            self.connection.commit()
            values = self.get_values(excel)
            for value in values:
                self.insert_data(excel, self.get_headlines()[i], value)
            print(f"Excel {excel} converted successfully")
            
    def get_headlines(self):
        headlines = []
        for excel in self.excels:
            df = pd.read_excel(f"excels/{excel}")
            headline = df.columns = [column.replace(" ", "_") for column in df.columns]
            headlines.append(headline)
        return headlines
    
    def get_values(self, excel):
        df = pd.read_excel(f"excels/{excel}")
        values = df.values.tolist()
        return values