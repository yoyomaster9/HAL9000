FROM python:3.9

WORKDIR /HAL9000

ADD ./cogs ./cogs
ADD ./craps ./craps
ADD ./resources ./resources
ADD ./main.py .
ADD ./config.py .

RUN pip install discord.py==1.7.3

CMD ["python", "-u", "/HAL9000/main.py"]