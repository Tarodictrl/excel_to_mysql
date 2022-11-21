import Converter

if __name__ == '__main__':
    host = 'localhost'
    password = ""
    user = ""
    excels = ["Oblast.xlsx", "Professii_1.xlsx"]
    converter = Converter.Converter(host, user, password, excels, "test")
    print(converter.convert_excels_to_sql())