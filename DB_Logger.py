import cx_Oracle


class DB_Logger:
    def __init__(self):
#        totally ugly way because messing with envvariables made my Oracle rip
#        and I failed configuring Oracle Wallet on XE database
        with open('magic.txt') as f:
            self.__client_path = f.readline().replace('\n', '')
            self.__pwd = f.readline()
#        cx_Oracle.init_oracle_client(lib_dir=self.__client_path)

    def open_connection(self):
        self.__conn = cx_Oracle.connect(dsn='SIM_APP_LOGS',
                                        user='SIM_APP_LOGGER',
                                        password=self.__pwd)

    def log_sim_step(self, state_dict):
        sql = self.build_log_sql(state_dict)

    def build_log_sql(self, state_dict):
        pass
