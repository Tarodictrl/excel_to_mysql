import Converter

if __name__ == '__main__':
    host = 'localhost'
    password = ""
    user = ""
    excels = ["Oblast.xlsx", "Professii_1.xlsx"]
    database_name = "test"
    converter = Converter.Converter(host, user, password, excels, database_name)
    converter.convert_excels_to_sql()