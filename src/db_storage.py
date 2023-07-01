from src.hh_parser import HeadHunterAPI

class DB_Storage:

    def insert_db(db_manager, api_head_hunter):
        """insert data base from api head hunter"""
        data = api_head_hunter.get_employers_vacancies()
        db_manager.insert_employers_vacancies_db(data)


# if __name__ == '__main__':
    # name_db = input("Введите имя базы данных: ")
    # create_db(name_db)
    # api = HeadHunterAPI()
    # db_manager = DBManager()
    # insert_db(db_manager, api)