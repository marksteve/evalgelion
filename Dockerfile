FROM ubuntu
RUN apt-get -y install build-essential
RUN apt-get -y install libffi-dev libcap-dev
RUN apt-get -y install python-dev python-setuptools
RUN easy_install pip
RUN pip install --no-use-wheel python-prctl cffi pyaib
ADD . /evalgelion
ENTRYPOINT ["python", "/evalgelion/evalgelion.py"]
