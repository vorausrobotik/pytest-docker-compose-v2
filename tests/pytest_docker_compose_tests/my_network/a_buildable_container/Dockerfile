FROM python:3.11.8-bookworm

WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY an_api.py /src/

# Expose 5001 as unused ports for testing purposes
EXPOSE 5000 5001
CMD ["python", "/src/an_api.py"]
