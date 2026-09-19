from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from sqlalchemy import text
from app.routers import (topics_router, contents_router)


app = FastAPI()

app.include_router(topics_router.router)
app.include_router(contents_router.router)



@app.get("/health")
async def healthcheck(db: Annotated[AsyncSession, Depends(get_session)]):
    try:

        result = await db.execute(text("SELECT 1 "))
        result.scalar()

        return{"status": "success", "database": "connected"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database connection failed: {str(e)}"
                            )







if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
