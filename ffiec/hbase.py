import happybase
import logging

#TODO tune these definitions
REPORT_TABLE = 'report'
REPORT_TABLE_DEFINITION = {'CallReport': dict(), 'Institution': dict()}

PERIOD_TABLE = 'period'
PERIOD_TABLE_DEFINITION = {'Institution': dict()}

INSTITUTION_TABLE = 'institution'
INSTITUTION_TABLE_DEFINITION = {'Period': dict()}

DATA_DICTIONARY = 'dictionary'
DATA_DICTIONARY_DEFINITION = {'Metadata': dict()}


class Hbase:
    def __init__(self, thrift_gateway, thrift_port):
        self.thrift_gateway = thrift_gateway
        self.thrift_port = thrift_port
        self.connection = None

    def connect(self):
        self.connection = happybase.Connection(host=self.thrift_gateway, port=self.thrift_port)

    @property
    def report_table(self):
        return self.connection.table(REPORT_TABLE)

    @property
    def period_table(self):
        return self.connection.table(PERIOD_TABLE)

    @property
    def institution_table(self):
        return self.connection.table(INSTITUTION_TABLE)

    @property
    def data_dictionary_table(self):
        return self.connection.table(DATA_DICTIONARY)

    def _disable_table(self, table):
        try:
            self.connection.disable_table(table)
            logging.debug('disabled table {}'.format(table))
        except Exception as err:
            logging.error(err)

    def _delete_table(self, table):
        try:
            self.connection.delete_table(table)
        except Exception as err:  # FIXME - built thrift objects and make this correct
            logging.error(err)

    def _create_table(self, table, definition):
        try:
            self.connection.create_table(table, definition)
        except Exception as err:
            logging.error(err)
            raise err

    def delete_dictionary_table(self):
        self._disable_table(DATA_DICTIONARY)
        self._delete_table(DATA_DICTIONARY)
        logging.warning('deleted MDRM dictionary tables')

    def create_dictionary_table(self):
        self._create_table(DATA_DICTIONARY, DATA_DICTIONARY_DEFINITION)
        logging.warning('created metadata tables')

    def delete_report_table(self):
        self._disable_table(REPORT_TABLE)
        self._delete_table(REPORT_TABLE)
        logging.warning('deleted report table')

    def create_report_table(self):
        self._create_table(REPORT_TABLE, REPORT_TABLE_DEFINITION)
        logging.warning('created report table')

    def delete_lookup_tables(self):
        for table in (PERIOD_TABLE, INSTITUTION_TABLE):
            self._disable_table(table)
            self._delete_table(table)
        logging.warning('deleted lookup tables')

    def create_lookup_tables(self):
        for table, definition in ((PERIOD_TABLE, PERIOD_TABLE_DEFINITION),
                                  (INSTITUTION_TABLE, INSTITUTION_TABLE_DEFINITION)):
            self._create_table(table, definition)
        logging.warning('created lookup tables')
