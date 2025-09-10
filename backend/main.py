from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from pathlib import Path
import os
import uvicorn

from app.routers import auth, tests, analysis

app = FastAPI(title="PYQ Practice Platform API", 
              description="API for Practice Platform for MCQ Questions", 
              version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(tests.router, prefix="/api", tags=["Tests"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])

# Get the absolute path to the frontend directory
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"

# Mount the frontend static files
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
app.mount("/css", StaticFiles(directory=Path(frontend_dir) / "css"), name="css")
app.mount("/js", StaticFiles(directory=Path(frontend_dir) / "js"), name="js")

@app.get("/", tags=["Root"])
async def root():
    """Serve the index.html file"""
    return FileResponse(Path(frontend_dir) / "index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    """Serve the favicon"""
    return FileResponse(Path(frontend_dir) / "favicon.ico")

@app.get("/apple-touch-icon.png", include_in_schema=False)
async def get_apple_touch_icon():
    """Serve the Apple touch icon"""
    return FileResponse(Path(frontend_dir) / "apple-touch-icon.png")

@app.get("/apple-touch-icon-precomposed.png", include_in_schema=False)
async def get_apple_touch_icon_precomposed():
    """Serve the Apple touch icon precomposed"""
    return FileResponse(Path(frontend_dir) / "apple-touch-icon-precomposed.png")

@app.get("/auth.js", include_in_schema=False)
async def redirect_auth_js():
    """Redirect to the correct auth.js path"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/js/auth.js", status_code=301)

# Add routes for other HTML files
@app.get("/signup", response_class=HTMLResponse)
async def signup():
    return FileResponse(Path(frontend_dir) / "signup.html")

@app.get("/login", response_class=HTMLResponse)
async def login():
    return FileResponse(Path(frontend_dir) / "login.html")

@app.post("/api/form-login")
async def form_login(request: Request):
    """Handle form login submissions and redirect to dashboard with a cookie"""
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    # Try to authenticate the user
    from app.services.auth_service import authenticate_user, create_access_token
    from datetime import timedelta
    
    user = authenticate_user(username, password)
    if not user:
        # If authentication fails, redirect back to login with an error parameter
        return RedirectResponse(url="/login?error=1", status_code=303)
    
    # Create token
    from app.services.auth_service import ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Create a response that redirects to dashboard
    response = RedirectResponse(url="/dashboard", status_code=303)
    
    # Set a cookie with the token
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,  # 30 minutes in seconds
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )
    
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return FileResponse(Path(frontend_dir) / "dashboard.html")

@app.get("/test", response_class=HTMLResponse)
async def test():
    return FileResponse(Path(frontend_dir) / "test.html")

@app.get("/results", response_class=HTMLResponse)
async def results():
    return FileResponse(Path(frontend_dir) / "results.html")

# Serve JS files
@app.get("/js/{file_path:path}", response_class=FileResponse)
async def serve_js(file_path: str):
    return FileResponse(Path(frontend_dir) / "js" / file_path)

# Serve CSS files
@app.get("/css/{file_path:path}", response_class=FileResponse)
async def serve_css(file_path: str):
    return FileResponse(Path(frontend_dir) / "css" / file_path)

# Serve auth.js directly at the root for compatibility
@app.get("/auth.js", response_class=FileResponse)
async def serve_auth_js():
    return FileResponse(Path(frontend_dir) / "js" / "auth.js")

# Serve style.css directly at the root for compatibility
@app.get("/style.css", response_class=FileResponse)
async def serve_style_css():
    return FileResponse(Path(frontend_dir) / "css" / "style.css")

# Serve favicon.ico
@app.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    return FileResponse(Path(frontend_dir) / "favicon.ico")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
