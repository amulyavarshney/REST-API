import uvicorn

# the main function to run the backend
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8081, reload=True)