FROM python:3.12

RUN apt update && apt upgrade -y

RUN apt install libpcap0.8 libpcap0.8-dev libpcap-dev tcpdump -y

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

CMD ["fastapi", "run", "main.py"]