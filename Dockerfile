# 1. Base Image: The grader strictly requires ubuntu:22.04 [cite: 263]
FROM ubuntu:22.04

# Prevent interactive prompts during apt-get installations
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install Python 3 and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file and install them
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your entire application code into the container
COPY . .

# 2. Port Binding: Port 8000 must be exported so the grader can hit your API [cite: 265]
EXPOSE 8000

# 3. Execution: Run the Uvicorn server, binding to 0.0.0.0 and NOT just localhost [cite: 266]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]