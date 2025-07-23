import ControlNode
import CollectorNode
import multiprocessing
import uvicorn

def start_service(service: str, port: int):
    uvicorn.run(service, host="127.0.0.1", port=port, reload=False)

services: list[tuple[str, int]] = [
    ("ControlNode.main:app", 8000),
    ("CollectorNode.main:app", 8001)
]

if __name__ == "__main__":
    processes: list[multiprocessing.Process] = []
    for s, p in services:
        starter = lambda: start_service(s, p)
        process: multiprocessing.Process = multiprocessing.Process(target=starter)
        process.start()
        processes.append(process)

    for proc in processes:
        proc.join()
