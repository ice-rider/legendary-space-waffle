import time
from http import HTTPStatus

from flask import request

from ..models import FileModel

from .api import BaseResource


class UploadFileResource(BaseResource):
    path = "/file"

    @classmethod
    def get(cls):
        id = request.args.get("file_id")

        if not id:
            return {"error": "no file_id in params, EBLAN"}, HTTPStatus.BAD_REQUEST
        
        file = FileModel.get_by_id(id)

        if not file:
            return {"file": None}, HTTPStatus.NOT_FOUND
        
        return {"file": file.json()}, HTTPStatus.OK
    
    @classmethod
    def post(cls):
        file = request.files['file']
        
        if not file:
            return {"error": "no file"}, HTTPStatus.BAD_REQUEST
        
        timestamp = time.time()
        extension = file.filename.split('.')[-1]

        try:
            path = f"/files/{timestamp}.{extension}"
            file.save(path)

            db_file = FileModel(
                filename = file.filename,
                url = f"/files/{path}"
            )
            return {
                "file": db_file.json()
            }
        except Exception as e:
            cls.logger.error(str(e))
            return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    