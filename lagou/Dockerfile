FROM python:3.9
WORKDIR /app
ADD lagou_data_analysis /app
ADD . /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5002
CMD ["python", "run.py"]