import ControlNode
import CollectorNode
import multiprocessing
import uvicorn
import os

def start_service(service: str, port: int):
    uvicorn.run(service, host="127.0.0.1", port=port, reload=False)

def start_ui(file = "../Ui/main.py"):
    os.system(f"streamlit run {file} --server.port 8501")

services: list[tuple[str, int]] = [
    ("ControlNode.main:app", 8000),
    ("CollectorNode.main:app", 8001),
    ("UiNode.main:app", 8012)
]

if __name__ == "__main__":
    processes: list[multiprocessing.Process] = []
    for s, p in services:
        starter = lambda: start_service(s, p)
        process: multiprocessing.Process = multiprocessing.Process(target=starter)
        process.start()
        processes.append(process)

    ui_process = multiprocessing.Process(target=start_ui)
    ui_process.start()
    processes.append(ui_process)

    for proc in processes:
        proc.join()


