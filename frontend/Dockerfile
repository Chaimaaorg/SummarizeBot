FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir streamlit

EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
