from http import HTTPStatus

from flask import request

from ..models import CommentModel

from .api import BaseResource


class CommentResource(BaseResource):
    path = "/comment"

    @classmethod
    def get(cls):
        comment_id = request.args.get("comment_id")
        card_id = request.args.get("card_id")

        if not all([card_id, comment_id]):
            return {"error": "comment_id or card_id is required arg"}, HTTPStatus.BAD_REQUEST
    
        if comment_id:
            comment = CommentModel.get_by_id(comment_id)
        else:
            comments = CommentModel.get_by_card_id(card_id)

        if (comment_id and not comment) or (card_id and not comments):
            return {"error": "comment not found"}, HTTPStatus.NOT_FOUND
        
        if comment_id:
            return {"comment": comment.json()}, HTTPStatus.OK
        else:
            return {"comments": [comment.json() for comment in comments]}, HTTPStatus.OK

    @classmethod
    def post(cls):
        args = request.get_json()

        username = args.get("username")
        message = args.get("message")
        card_id = args.get("card_id")

        if not all([username, message, card_id]):
            return {"error": "username, message, card_id is required args, UEBOK"}, HTTPStatus.BAD_REQUEST

        try:
            comment = CommentModel(
                card_id = card_id,
                username = username,
                mesage = message
            )
            comment.save()
            return {"comment": comment.json()}, HTTPStatus.CREATED
    
        except Exception as e:
            cls.logger.error(str(e))
            return {"error": str(e) + ", EBBLANISHE TUPOE!"}, HTTPStatus.CONFLICT