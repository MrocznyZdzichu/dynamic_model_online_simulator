import utils
import cx_Oracle


class DB_Logger:
    def __init__(self):
        #\totally ugly way because I failed configuring Oracle Wallet on XE database
        #totally ugly way because messing with envvariables made my Oracle rip
        with open('magic.txt') as f:
            self.__client_path = f.readline().replace('\n', '')
            self.__pwd = f.readline()
            cx_Oracle.init_oracle_client(lib_dir=self.__client_path)

    log_tab = 'SIM_LOGS.SIM_STEPS_LOGS'

    def log_sim_step(self, state_dict):
        sql = self.__build_log_sql(state_dict)
        self.__open_connection()
        self.__fire_insert(sql)
        self.__close_connection()

    def __open_connection(self):
        self.__conn = cx_Oracle.connect(dsn='SIM_APP_LOGS',
                                        user='SIM_APP_LOGGER',
                                        password=self.__pwd)
        self.__crsr = self.__conn.cursor()

    def __close_connection(self):
        self.__conn.close()

    def __build_log_sql(self, state_dict):
        sql = f"insert into {self.log_tab} values (\n"
        for column in state_dict.keys():
            sql += f'{state_dict[column]}, '

        sql = utils.trim_trailing_symbol(sql, ', ')
        sql += '\n)'
        return sql

    def __fire_insert(self, sql):
        self.__crsr.execute(sql)
        self.__conn.commit()
