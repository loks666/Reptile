FROM python:3.9
WORKDIR /app
ADD . /app
ENV PYTHONPATH="/app:$PYTHONPATH"
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r lagou_data_analysis/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple pymysql
EXPOSE 5002
CMD ["python", "run.py"]
