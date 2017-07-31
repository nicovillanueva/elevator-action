FROM python:3.6.2-alpine3.6

ADD elevatoraction/ /data/elevatoraction/
ADD main.py /data/
ADD tests.py /data/
WORKDIR /data/

ENTRYPOINT ["python3"]
CMD ["-m", "unittest" , "/data/tests.py"]