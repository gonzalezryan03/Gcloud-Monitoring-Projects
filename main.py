from flask import Flask, render_template
from google.cloud import monitoring_v3
import time
import threading

app = Flask(__name__)
project_id = "cloud-monitoring-learning"
metric_type = "custom.googleapis.com/myapp/requests_count"
client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

def create_metric_descriptor():
    descriptor = monitoring_v3.MetricDescriptor()
    descriptor.type = metric_type
    descriptor.display_name = "My App Requests Count"
    descriptor.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64
    descriptor.description = "Number of requests processed by the app"
    descriptor.unit = "1"
    descriptor.labels = [monitoring_v3.LabelDescriptor(key="app_version", description="App version")]

    client.create_metric_descriptor(project_name, descriptor)

def write_time_series(value):
    series = monitoring_v3.TimeSeries()
    series.metric.type = metric_type
    series.resource.type = "global"
    series.resource.labels["project_id"] = project_id
    series.metric.labels["app_version"] = "1.0.0"
    current_time = time.time()
    
    point = monitoring_v3.Point({
        "value": {"int64_value": value},
        "interval": {
            "end_time": {"seconds": int(current_time)}
        }
    })
    series.points = [point]
    
    request = monitoring_v3.CreateTimeSeriesRequest(
        name=project_name,
        time_series=[series]
    )
    
    client.create_time_series(request)

def push_metrics_periodically():
    count = 0
    while True:
        write_time_series(count)
        count += 1
        time.sleep(30)

@app.route("/")
def home():
    return "Hello from the Monitoring Microservice!"

if __name__ == "__main__":
    try:
        create_metric_descriptor()
    except Exception as e:
        print(f"Error: {e}")

    threading.Thread(target=push_metrics_periodically).start()
    app.run(host="0.0.0.0", port=8080)
