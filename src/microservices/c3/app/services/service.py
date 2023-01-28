from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from cryptography import fernet

from app.schemas.schema import (
    LabelORMSchema, ExchangeSymbolLabelORMSchema,
    ExchangeTickerLabelORMSchema, ExchangeTickerORMSchema
)
from app.orm.cfg.engine import ORMSettings
from app.cfg.settings import settings
from app.orm import base


class C3Service:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
        self._fn = fernet.Fernet(key=settings.JWT_FERNET_KEY)

    def _get_h_exchange_by_name(self, exchange_name: str) -> Optional[base.hExchanges]:
        return self._session.query(base.hExchanges).filter_by(h_exchange_name=exchange_name).first()

    def _get_h_label_by_name(self, label_name: str) -> Optional[base.hLabels]:
        return self._session.query(base.hLabels).filter_by(h_label_name=label_name).first()

    def _get_h_ticker_by_name(self, ticker_name: str) -> Optional[base.hTickers]:
        return self._session.query(base.hTickers).filter_by(h_ticker_name=ticker_name).first()

    def _get_h_symbol_by_name(self, symbol_name: str) -> Optional[base.hSymbols]:
        return self._session.query(base.hSymbols).filter_by(h_symbol_name=symbol_name).first()

    def _get_l_exchange_symbol(self, exchange_name: str, symbol_name: str) -> Optional[base.lExchangesSymbols]:
        h_exchange, h_symbol = self._get_h_exchange_by_name(exchange_name=exchange_name), self._get_h_symbol_by_name(symbol_name=symbol_name)
        if not h_exchange or not h_symbol:
            return None
        return self._session.query(base.lExchangesSymbols).filter_by(
            h_exchange_id=h_exchange.h_exchange_id,
            h_symbol_id=h_symbol.h_symbol_id
        ).first()

    def _get_l_exchange_ticker(self, exchange_name: str, ticker_name: str) -> Optional[base.lExchangesTickers]:
        h_exchange, h_ticker = self._get_h_exchange_by_name(exchange_name=exchange_name), self._get_h_ticker_by_name(ticker_name=ticker_name)
        if not h_exchange or not h_ticker:
            return None
        return self._session.query(base.lExchangesTickers).filter_by(
            h_exchange_id=h_exchange.h_exchange_id,
            h_ticker_id=h_ticker.h_ticker_id
        ).first()

    def _get_l_exchange_symbol_label(self, exchange_name: str, symbol_name: str, label_name: str) -> Optional[base.lExchangesSymbolsLabels]:
        l_exchange_symbol, h_label = self._get_l_exchange_symbol(exchange_name=exchange_name, symbol_name=symbol_name), self._get_h_label_by_name(label_name=label_name)
        if not l_exchange_symbol or not h_label:
            return None
        return self._session.query(base.lExchangesSymbolsLabels).filter_by(
            l_exchange_symbol_id=l_exchange_symbol.l_exchange_symbol_id,
            h_label_id=h_label.h_label_id
        ).first()

    def _get_l_exchange_ticker_label(self, exchange_name: str, ticker_name: str, label_name: str) -> Optional[base.lExchangesTickersLabels]:
        l_exchange_ticker, h_label = self._get_l_exchange_ticker(exchange_name=exchange_name, ticker_name=ticker_name), self._get_h_label_by_name(label_name=label_name)
        if not l_exchange_ticker or not h_label:
            return None
        return self._session.query(base.lExchangesTickersLabels).filter_by(
            l_exchange_ticker_id=l_exchange_ticker.l_exchange_ticker_id,
            h_label_id=h_label.h_label_id
        ).first()

    def _insert_h_label(self, label_name: str, label_api_key: str, label_api_secret: str) -> base.hLabels:
        h_label = self._get_h_label_by_name(label_name=label_name)
        if not h_label:
            h_label = base.hLabels(
                h_label_name=label_name,
                h_label_api_key=label_api_key,
                h_label_secret_key=label_api_secret
            )
            self._session.add(h_label)
            self._session.commit()
        return h_label

    def _insert_h_exchange(self, exchange_name: str) -> base.hExchanges:
        h_exchange = self._get_h_exchange_by_name(exchange_name=exchange_name)
        if not h_exchange:
            h_exchange = base.hExchanges(
                h_exchange_name=exchange_name
            )
            self._session.add(h_exchange)
            self._session.commit()
        return h_exchange

    def _insert_h_symbol(self, symbol_name: str) -> base.hSymbols:
        h_symbol = self._get_h_symbol_by_name(symbol_name=symbol_name)
        if not h_symbol:
            h_symbol = base.hSymbols(
                h_symbol_name=symbol_name
            )
            self._session.add(h_symbol)
            self._session.commit()
        return h_symbol

    def _insert_h_ticker(self, ticker_name: str) -> base.hTickers:
        h_ticker = self._get_h_ticker_by_name(ticker_name=ticker_name)
        if not h_ticker:
            h_ticker = base.hTickers(
                h_ticker_name=ticker_name
            )
            self._session.add(h_ticker)
            self._session.commit()
        return h_ticker

    def _insert_l_exchange_symbol(self, exchange_name: str, symbol_name: str) -> base.lExchangesSymbols:
        h_exchange, h_symbol = self._insert_h_exchange(exchange_name=exchange_name), self._insert_h_symbol(symbol_name=symbol_name)

        l_exchange_symbol = self._get_l_exchange_symbol(exchange_name=h_exchange.h_exchange_name, symbol_name=h_symbol.h_symbol_name)
        if not l_exchange_symbol:
            l_exchange_symbol = base.lExchangesSymbols(
                h_exchange_id=h_exchange.h_exchange_id,
                h_symbol_id=h_symbol.h_symbol_id
            )
            self._session.add(l_exchange_symbol)
            self._session.commit()
        return l_exchange_symbol

    def _insert_l_exchange_ticker(self, exchange_name: str, ticker_name: str) -> base.lExchangesTickers:
        h_exchange, h_ticker = self._insert_h_exchange(exchange_name=exchange_name), self._insert_h_ticker(ticker_name=ticker_name)

        l_exchange_ticker = self._get_l_exchange_ticker(exchange_name=h_exchange.h_exchange_name, ticker_name=h_ticker.h_ticker_name)
        if not l_exchange_ticker:
            l_exchange_ticker = base.lExchangesTickers(
                h_exchange_id=h_exchange.h_exchange_id,
                h_ticker_id=h_ticker.h_ticker_id
            )
            self._session.add(l_exchange_ticker)
            self._session.commit()
        return l_exchange_ticker

    def _insert_l_exchange_symbol_label(self, exchange_name: str, symbol_name: str, label_name: str) -> Optional[base.lExchangesSymbolsLabels]:
        h_exchange, h_symbol, h_label = self._insert_h_exchange(
            exchange_name=exchange_name
        ), self._insert_h_symbol(
            symbol_name=symbol_name
        ), self._get_h_label_by_name(label_name=label_name)

        if not h_label:
            return None

        l_exchange_symbol_label = self._get_l_exchange_symbol_label(exchange_name=h_exchange.h_exchange_name, symbol_name=h_symbol.h_symbol_name, label_name=h_label.h_label_name)
        if not l_exchange_symbol_label:
            l_exchange_symbol = self._insert_l_exchange_symbol(exchange_name=h_exchange.h_exchange_name, symbol_name=h_symbol.h_symbol_name)

            l_exchange_symbol_label = base.lExchangesSymbolsLabels(
                h_label_id=h_label.h_label_id,
                l_exchange_symbol_id=l_exchange_symbol.l_exchange_symbol_id
            )
            self._session.add(l_exchange_symbol_label)
            self._session.commit()
        return l_exchange_symbol_label

    def _insert_l_exchange_ticker_label(self, exchange_name: str, ticker_name: str, label_name: str) -> Optional[base.lExchangesTickersLabels]:
        h_exchange, h_ticker, h_label = self._insert_h_exchange(
            exchange_name=exchange_name
        ), self._insert_h_ticker(
            ticker_name=ticker_name
        ), self._get_h_label_by_name(label_name=label_name)

        if not h_label:
            return None

        l_exchange_ticker_label = self._get_l_exchange_ticker_label(exchange_name=h_exchange.h_exchange_name, ticker_name=h_ticker.h_ticker_name, label_name=h_label.h_label_name)
        if not l_exchange_ticker_label:
            l_exchange_ticker = self._insert_l_exchange_ticker(exchange_name=h_exchange.h_exchange_name, ticker_name=h_ticker.h_ticker_name)

            l_exchange_ticker_label = base.lExchangesTickersLabels(
                h_label_id=h_label.h_label_id,
                l_exchange_ticker_id=l_exchange_ticker.l_exchange_ticker_id
            )
            self._session.add(l_exchange_ticker_label)
            self._session.commit()
        return l_exchange_ticker_label

    def _hash_by_fernet(self, value: str) -> str:
        return self._fn.encrypt(value.encode()).decode()

    def on_post__new_account(self, label_name: str, label_api_key: str, label_api_secret: str) -> LabelORMSchema:
        h_label = self._insert_h_label(
            label_name=label_name,
            label_api_key=self._hash_by_fernet(value=label_api_key),
            label_api_secret=self._hash_by_fernet(value=label_api_secret)
        )
        return LabelORMSchema.from_orm(h_label)

    def on_post__new_account_balances(self, label_name: str, exchange_name: str, symbol_name: str) -> Optional[ExchangeSymbolLabelORMSchema]:
        l_exchange_symbol_label = self._insert_l_exchange_symbol_label(
            exchange_name=exchange_name,
            symbol_name=symbol_name,
            label_name=label_name
        )
        return ExchangeSymbolLabelORMSchema.from_orm(l_exchange_symbol_label) if l_exchange_symbol_label else None

    def on_post__new_account_limit_orders(self, label_name: str, exchange_name: str, ticker_name: str) -> Optional[ExchangeTickerLabelORMSchema]:
        l_exchange_ticker_label = self._insert_l_exchange_ticker_label(
            exchange_name=exchange_name,
            ticker_name=ticker_name,
            label_name=label_name
        )
        return ExchangeTickerLabelORMSchema.from_orm(l_exchange_ticker_label) if l_exchange_ticker_label else None

    def on_post__new_account_liquidations(self, label_name: str, exchange_name: str, ticker_name: str) -> Optional[ExchangeTickerLabelORMSchema]:
        return self.on_post__new_account_limit_orders(label_name=label_name, exchange_name=exchange_name, ticker_name=ticker_name)

    def on_post__new_whole_market_trades_history(self, exchange_name: str, ticker_name: str) -> ExchangeTickerORMSchema:
        l_exchange_ticker = self._insert_l_exchange_ticker(
            exchange_name=exchange_name,
            ticker_name=ticker_name
        )
        return ExchangeTickerORMSchema.from_orm(l_exchange_ticker)


