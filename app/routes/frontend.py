from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

router = APIRouter(include_in_schema=False)

@router.get("/", response_class=FileResponse)
async def get_index():
    return FileResponse("static/index.html",media_type='text/html')


@router.get("/check", response_class=FileResponse)
async def get_check():
    return FileResponse("static/check.html", media_type='text/html')
