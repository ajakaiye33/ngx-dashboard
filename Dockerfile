FROM python:3.8.13-slim-buster
EXPOSE 8501
WORKDIR /stock_viz
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run stock_viz.py