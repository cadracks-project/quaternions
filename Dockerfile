FROM continuumio/miniconda3:4.4.10

MAINTAINER Guillaume Florent <florentsailing@gmail.com>

RUN conda install -y numpy pytest

WORKDIR /opt
ADD https://api.github.com/repos/osv-team/quaternions/git/refs/heads/master version.json
RUN git clone --depth=1 https://github.com/osv-team/quaternions

WORKDIR /opt/quaternions
RUN python setup.py install