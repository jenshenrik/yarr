FROM python:3.8-slim-buster
ADD roguelike.py /
RUN apt update && apt install build-essential python3-dev python3-pip python3-numpy libsdl2-dev libffi-dev libomp5 -y
RUN pip install tcod
CMD ["python", "roguelike.py"]
