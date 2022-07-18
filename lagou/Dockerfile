FROM python:3.9

WORKDIR /app/lagou
ADD . /app/lagou

RUN pip install -r lagou_data_analysis/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple pymysql

EXPOSE 5002

ENV PYTHONPATH="/app:$PYTHONPATH"

CMD ["python", "./lagou_data_analysis/run.py"]
