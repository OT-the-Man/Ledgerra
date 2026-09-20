FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY run_pipeline.py pull_multi.py load_all_to_sqlite.py phase1_analysis.py phase2_analysis.py ./
CMD ["python", "run_pipeline.py"]