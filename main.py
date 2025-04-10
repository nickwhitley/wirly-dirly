from api.oanda_api import OandaApi
from infrastructure.instrument_collection import InstrumentCollection
from infrastructure import data_collection
from backtesting import backtesting



if __name__ == '__main__':

    api = OandaApi()
    instument_collection = InstrumentCollection(api)
    # instument_collection.load_instruments('./data')
    # data_collection.run_collection(instument_collection, api)
    pairs = ["AUD_USD", "EUR_USD", "GBP_USD", "USD_CHF", "USD_JPY", "NZD_USD", "USD_CAD"]
    granularities = ["H1"]
    backtesting.run_wirly_dirly_test(pairs, granularities, instument_collection)

