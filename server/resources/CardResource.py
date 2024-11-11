from http import HTTPStatus

from flask import request

from ..models import CardModel

from .api import BaseResource


class CardResource(BaseResource):
    path = "/card"

    @classmethod
    def get(cls):
        id = request.args.get("card_id")

        if not id:
            return {"error": "no card_id in params, EBLAN"}, HTTPStatus.BAD_REQUEST
        
        card = CardModel.get_by_id(id)
        
        if not card:
            return {"card": None}, HTTPStatus.NOT_FOUND

        return {"card": card.json()}, HTTPStatus.OK
    
    @classmethod
    def post(cls):
        args = request.get_json()
        data = dict()

        for arg in ["title", "description", "deadline", "budget", "worker_price", "worker_name", "worker_url", "customer_name", "customer_url", "file_id"]:
            if args.get(arg) is None:
                return {"error", f"arg {arg} is required, EBLAN!"}, HTTPStatus.BAD_REQUEST
            data[arg] = args.get(arg)

        try:
            card = CardModel(**data)
            card.save()
            return {"card": card.json()}, HTTPStatus.CREATED
       
        except Exception as e:
            cls.logger.error(str(e))
            return {"error": str(e) + ", EBLAN!"}, HTTPStatus.BAD_REQUEST

    @classmethod
    def put(cls):
        args = request.get_json()
        data = dict()

        for arg in ["card_id", "title", "description", "status", "deadline", "budget", "worker_price", "worker_name", "worker_url", "customer_name", "customer_url", "file_id"]:
            data[arg] = args.get(arg)

        try:
            card = CardModel.get_by_id(data["card_id"])
            card.put(**data)
            card.save()
            return {"card": card.json()}, HTTPStatus.OK

        except Exception as e:
            cls.logger.error(str(e))
            return {"error": str(e) + ", EBLAN!"}, HTTPStatus.BAD_REQUEST

    @classmethod
    def delete(cls):
        args = request.get_json()

        card_id = args.get("card_id")

        if not card_id:
            return {"error": "card_id is required arg, EBLAN!"}, HTTPStatus.BAD_REQUEST
        
        card = CardModel.get_by_id(card_id)

        if not card:
            return {"error": "card not found, EBLANISHE TUPOE!"}, HTTPStatus.NOT_FOUND
        
        card.delete()

        return {"message": "successfully removed card"}, HTTPStatus.OK


class CardListResource(BaseResource):
    path = "/card/list"

    @classmethod
    def get(cls):
        cards = CardModel.query.all()
        if not cards:
            return {"error": "cards not found"}, HTTPStatus.NOT_FOUND
        
        return {"cards": [card.json() for card in cards]}, HTTPStatus.OK