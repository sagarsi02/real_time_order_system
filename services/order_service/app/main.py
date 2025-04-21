from fastapi import FastAPI

app = FastAPI(title="Order Service")

@app.get("/")
def root():
    return {"message": "Order Service is running"}
