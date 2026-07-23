from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from app.libgen import LibGenClient
from app.models import SearchResponse

router = APIRouter()

client = LibGenClient()


@router.get(
    "/search",
    response_model=SearchResponse,
    tags=["Books"]
)
async def search(q: str):

    books = client.search(q)

    return SearchResponse(
        total=len(books),
        books=books
    )

@router.get("/cover/{md5}")
async def cover(md5:str):

    url = client.cover(md5)

    return {
        "cover":url
    }

@router.get(
    "/download/{md5}",
    tags=["Books"]
)

async def download(md5: str):

    try:

        archive = client.download(md5)

        headers = {
            "Content-Disposition":
                archive.headers.get(
                    "Content-Disposition",
                    "attachment"
                )
        }

        return StreamingResponse(
            archive.iter_content(8192),
            media_type=archive.headers.get(
                "Content-Type",
                "application/octet-stream"
            ),
            headers=headers
        )

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )