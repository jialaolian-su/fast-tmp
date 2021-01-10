FROM python:3.8
RUN mkdir -p /src
RUN mkdir ~/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple\nformat = columns" > ~/.pip/pip.conf
WORKDIR /src
COPY poetry.lock pyproject.toml /src/
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip3 install poetry
RUN poetry install
COPY . /src