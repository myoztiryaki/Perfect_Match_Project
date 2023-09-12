conda create -n astro-env python=3.8
conda activate astro-env
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
