import logging
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def install(app):
    @app.exception_handler(HTTPException)
    async def http_error(request,exc):
        codes={401:'unauthorized',403:'forbidden',404:'not_found',409:'conflict'}
        return JSONResponse(status_code=exc.status_code,content={'error':{'code':codes.get(exc.status_code,'http_error'),'message':str(exc.detail),'details':{}}},headers=exc.headers)
    @app.exception_handler(RequestValidationError)
    async def validation(request,exc):
        return JSONResponse(status_code=422,content={'error':{'code':'validation_error','message':'Invalid input','details':jsonable_encoder(exc.errors(),custom_encoder={ValueError:str})}})
    @app.exception_handler(Exception)
    async def unexpected(request,exc):
        logging.getLogger(__name__).error('Unhandled error',exc_info=exc)
        return JSONResponse(status_code=500,content={'error':{'code':'internal_error','message':'Internal error','details':{}}})
