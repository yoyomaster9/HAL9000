FROM python:3.9

# Need to add all relavent .py files

ADD ./cogs /HAL9000/cogs
ADD ./craps /HAL9000/craps
ADD ./resources /HAL9000/resources
ADD ./main.py /HAL9000
ADD ./config.py /HAL9000

RUN pip install discord.py==1.7.3

CMD ["python", "/HAL9000/main.py"]