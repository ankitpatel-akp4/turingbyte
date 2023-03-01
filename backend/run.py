import uvicorn
if __name__ == '__main__':
    uvicorn.run("src.main:app", port=8000, host='127.0.0.1',reload=True)