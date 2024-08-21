
# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the app files
COPY . .

# Expose the port the app will run on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "stock_viz.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
