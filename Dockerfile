# Use the official Streamlit image as the base image
FROM streamlit/streamlit:latest

# Install additional packages
RUN pip install feedparser

# Set the working directory
WORKDIR /app

# Copy the Streamlit app into the container
COPY pxgraph.py .

# Set the Streamlit command to run the app
CMD ["streamlit", "run", "pxgraph.py"]
