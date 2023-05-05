import json
import logging
from flask import Blueprint, request, Request, jsonify
import re
from backend.service.fintech import risk_parity

risk_parity_calculator = Blueprint('risk_parity_calculator', __name__)

risk_prefix = '/risk'


class RequestParameterException(BaseException):
    def __init__(self):
        self.messages: dict[str, str] = dict()

    def __len__(self) -> int:
        return len(self.messages)

    def push_message(self, column: str, message: str):
        self.messages[column] = message
        return self

    def missing_value(self, column: str):
        return self.push_message(
            column,
            'missing required value'
        )

    def wrong_format(self, column: str):
        return self.push_message(
            column,
            'wrong format'
        )

    def throw(self):
        if len(self.messages):
            raise self


class RiskParityRequest:
    START_DATE = 'start_date'
    END_DATE = 'end_date'
    ASSET = 'asset[]'
    PERIOD = 'period[]'

    @property
    def start_date(self) -> str:
        return self.args[self.START_DATE]

    @property
    def end_date(self) -> str:
        return self.args[self.END_DATE]

    @property
    def asset(self) -> list[str]:
        return self.args[self.ASSET]

    @property
    def period(self) -> list[int]:
        return self.args[self.PERIOD]

    def __init__(self, req: Request):
        self.exception: RequestParameterException = RequestParameterException()
        self.args: dict = dict()

        self._set_date(req, self.START_DATE)
        self._set_date(req, self.END_DATE)
        self._set_asset(req)
        self._set_period(req)

        self.exception.throw()

    def _set_asset(self, req: Request):
        logging.info(json.dumps(req.args))
        logging.info(json.dumps(req.args.getlist('{}[]'.format(self.ASSET))))

        if self.ASSET not in req.args:
            self.exception.missing_value(self.ASSET)
            return self

        self.args[self.ASSET] = req.args.getlist(self.ASSET)

        return self

    def _set_period(self, req: Request):
        if self.PERIOD not in req.args:
            self.exception.missing_value(self.PERIOD)
            return self

        self.args[self.PERIOD] = req.args.getlist(self.PERIOD)

        return self

    def _set_date(self, req: Request, column: str):
        value = req.args.get(column)

        if value is None:
            self.exception.missing_value(column)
            return self

        match = re.match(r'^(\d{4}-\d{2}-\d{2})$', value)

        if match is None:
            self.exception.missing_value(column)
            return self

        self.args[column] = value


@risk_parity_calculator.get(risk_prefix)
def calc_risk_parity():
    try:
        risk_parity_request = RiskParityRequest(request)

        response = {}
        for period in risk_parity_request.period:
            response[period] = risk_parity.calculate(
                start_date=risk_parity_request.start_date,
                end_date=risk_parity_request.end_date,
                assets=[risk_parity.Asset(asset) for asset in risk_parity_request.asset],
                period=period
            )

        return jsonify(**response)
    except RequestParameterException as e:
        return jsonify(
            error=e.messages
        ), 400
