import jaydebeapi
from ibmdbpy import IdaDataBase
from ibmdbpy import IdaDataFrame

idadb = IdaDataBase(
            'jdbc:db2://dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net:50000/BLUDB:user=wnb76963;password=9vb^gk46p02n0j9d')

class Db2:
    def __init__(self, table_name='INTERSTATE_TRAFFIC'):
        self.ida_traffic_pd = IdaDataFrame(idadb, table_name).as_dataframe()

    def last24hours(self):
        return self.ida_traffic_pd['traffic_volume'][-24:].values

    def last6hours(self):
        return self.ida_traffic_pd['traffic_volume'][-6:].values
