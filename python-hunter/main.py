"""Run the local workspace; no demo projects or mock execution."""
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web_tma.backend.server:app", host="127.0.0.1", port=4318)
