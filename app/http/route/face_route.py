import math
from typing import List
from venv import logger

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.http.controller.face_controller import FaceController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.face_schema import FaceResponse, AddFaceRequest, ListFaceRequest


def get_face_router():
    face_router = APIRouter()
    face_controller = FaceController()

    @face_router.post("/", response_model=WebResponse[FaceResponse], status_code=HTTP_201_CREATED)
    async def add(request: AddFaceRequest = Depends(AddFaceRequest.as_form), current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        # await request.file.read()
        if current_user:
            request.user_id = current_user
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        try:
            data = AddFaceRequest(**request.dict(exclude={"file"}), file=request.file)
            return face_controller.add(data, request.file)
        except HTTPException as err:
            logger.error(f"Error during add face: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @face_router.get("/", response_model=WebResponse[List[FaceResponse]], status_code=HTTP_200_OK)
    async def list(request: Request, current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)
        data = ListFaceRequest()
        try:
            if current_user:
                data.user_id = current_user
                data.page = int(page)
                data.size = int(size)

                result = face_controller.list(data)
                total = result["total"]
                paging = {
                    "page": data.page,
                    "size": data.size,
                    "total_item": total,
                    "total_page": int(math.ceil(total / data.size))
                }
                return WebResponse(data=result["data"], paging=paging)
            else:
                raise HTTPException(status_code=400, detail="Invalid user ID")
        except HTTPException as err:
            logger.error(f"Error during list face: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)


    return face_router