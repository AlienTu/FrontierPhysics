FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    MPLBACKEND=Agg

RUN pip install --no-cache-dir \
    numpy==2.1.3 \
    scipy==1.14.1 \
    matplotlib==3.9.2 \
    pytest==8.3.3 \
    pytest-json-ctrf==0.3.5

WORKDIR /root
RUN chmod 777 /root
