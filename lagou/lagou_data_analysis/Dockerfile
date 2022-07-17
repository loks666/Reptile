FROM python:3.9
WORKDIR /run
ADD . /run
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5002
CMD ["python", "run.py"]