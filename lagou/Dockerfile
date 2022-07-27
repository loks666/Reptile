FROM python:3.9

WORKDIR /app/lagou
ADD . /app/lagou
ADD ./lagou_data_analysis/data.json /app/lagou

ENV LANG en_US.UTF-8
RUN pip install -r lagou_data_analysis/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r pydevd-pycharm~=212.5457.59 -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5002
EXPOSE 5004
ENV PYTHONPATH="/app:$PYTHONPATH"

CMD ["python", "./lagou_data_analysis/run.py","-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005"]
