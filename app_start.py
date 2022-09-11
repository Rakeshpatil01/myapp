import uvicorn

if __name__ == '__main__':
    uvicorn.run("UserManagemenet.main:app", port=8080,
                host='localhost', debug=True, reload=True)
