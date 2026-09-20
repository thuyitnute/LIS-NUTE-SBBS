@echo off
call venv\Scripts\activate
python -m uvicorn smart_boxes.main:app --reload --port 55118
pause