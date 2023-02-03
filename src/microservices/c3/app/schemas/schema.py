from pydantic import BaseModel
from datetime import datetime


class LabelORMSchema(BaseModel):
    h_label_id: int
    h_label_name: str
    h_label_api_key: str
    h_label_secret_key: str
    h_label_load_ts: datetime

    class Config:
        orm_mode = True


class ExchangeTickerORMSchema(BaseModel):
    l_exchange_ticker_id: int
    h_exchange_id: int
    h_ticker_id: int
    l_exchange_ticker_load_ts: datetime

    class Config:
        orm_mode = True


class ExchangeSymbolLabelORMSchema(BaseModel):
    l_exchange_symbol_label_id: int
    h_label_id: int
    l_exchange_symbol_id: int
    l_exchange_symbol_label_load_ts: datetime

    class Config:
        orm_mode = True


class ExchangeTickerLabelORMSchema(BaseModel):
    l_exchange_ticker_label_id: int
    h_label_id: int
    l_exchange_ticker_id: int
    l_exchange_ticker_label_load_ts: datetime

    class Config:
        orm_mode = True


class NewLabelSchema(BaseModel):
    label_name: str
    label_api_key: str
    label_api_secret: str


class NewWholeMarketTradesHistory(BaseModel):
    exchange_name: str
    instrument_name: str


class NewAccountBalanceSchema(NewWholeMarketTradesHistory):
    label_name: str


class NewAccountLimitOrderSchema(NewAccountBalanceSchema): ...


class NewAccountLiquidationSchema(NewAccountLimitOrderSchema): ...
