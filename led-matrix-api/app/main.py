from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from app.controller import LedMatrixController
from app.schemas import SectionSchema
from app.auth import get_api_key

# Global controller instance
matrix_controller = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global matrix_controller
    try:
        matrix_controller = LedMatrixController()
        # Optionally clear on startup
        matrix_controller.clear()
        print("LED Matrix initialized and cleared.")
    except Exception as e:
        print(f"Failed to initialize LED Matrix: {e}")
        # We might want to re-raise or handle gracefully depending on requirements
        # For now, let's allow app startup but controller might be broken
    
    yield
    
    # Shutdown
    if matrix_controller:
        matrix_controller.clear()
        print("LED Matrix cleared on shutdown.")

app = FastAPI(
    title="LED Matrix API",
    description="API to control 32x16 LED Matrix divided into two sections.",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/section/{section_id}", dependencies=[Depends(get_api_key)])
async def set_section(section_id: int, data: SectionSchema):
    if matrix_controller is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Matrix controller not initialized"
        )
    
    if section_id not in [0, 1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid section ID. Must be 0 or 1."
        )

    try:
        matrix_controller.update_section(section_id, data.char, data.locked)
        return {"status": "success", "section": section_id, "data": data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/clear", dependencies=[Depends(get_api_key)])
async def clear_matrix():
    if matrix_controller is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Matrix controller not initialized"
        )
    
    try:
        matrix_controller.clear()
        return {"status": "success", "message": "Matrix cleared"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
