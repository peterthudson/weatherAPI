# Select base image
FROM python:3.9

# Add files
ADD main.py .
ADD resources.py .
ADD test_resources.py .

# Install dependencies
RUN pip3 install requests   
RUN pip3 install statistics
RUN pip3 install "fastapi[standard]"

# Run commands
CMD ["fastapi", "run", "main.py", "--port", "8000"]