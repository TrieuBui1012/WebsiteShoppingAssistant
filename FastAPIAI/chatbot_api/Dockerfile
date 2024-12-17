# FROM public.ecr.aws/amazonlinux/amazonlinux:latest
FROM python:3.11-slim

# RUN yum update -y && \
#  yum install -y httpd

WORKDIR /app
COPY ./src/ /app/src

# Set the PYTHONPATH to include the /app/src directory
ENV PYTHONPATH=/app/src

COPY ./pyproject.toml /code/pyproject.toml
RUN pip install /code/.

# Copy entrypoint.sh to the container
COPY ./src/entrypoint.sh /app/entrypoint.sh

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
CMD ["sh", "/app/entrypoint.sh"]

# # Base image for AWS Lambda Python 3.11 runtime
# FROM public.ecr.aws/lambda/python:3.11

# WORKDIR ${LAMBDA_TASK_ROOT}

# # Copy application source code
# COPY src/ ${LAMBDA_TASK_ROOT}/
# COPY src/.env ${LAMBDA_TASK_ROOT}/.env

# # Set the PYTHONPATH to include the ${LAMBDA_TASK_ROOT} directory
# ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

# # Copy Poetry configuration files
# # COPY ./pyproject.toml ${LAMBDA_TASK_ROOT}/pyproject.toml
# # RUN pip install ${LAMBDA_TASK_ROOT}/.
# # Copy and install dev dependencies (optional)
# # Copy requirements.txt to the container
# COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt

# # Install dependencies using pip
# RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# # Make the entrypoint script executable
# RUN chmod +x ${LAMBDA_TASK_ROOT}/entrypoint.sh
# # Expose the default FastAPI port for local testing
# EXPOSE 8000


# CMD ["lambda_handler.handler"]