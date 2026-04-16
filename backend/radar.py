import boto3
import pyart
import matplotlib.pyplot as plt
import os

BUCKET = "noaa-nexrad-level2"

def get_latest_scan(station="KLOT"):
    s3 = boto3.client("s3")

    prefix = f"{station}/"
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)

    files = sorted([obj["Key"] for obj in response.get("Contents", [])])
    latest = files[-1]

    local_file = f"/tmp/{latest.split('/')[-1]}"
    s3.download_file(BUCKET, latest, local_file)

    return local_file


def generate_image(product="reflectivity"):
    file_path = get_latest_scan()

    radar = pyart.io.read(file_path)

    display = pyart.graph.RadarDisplay(radar)

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111)

    field_map = {
        "REF": "reflectivity",
        "VEL": "velocity",
        "CC": "cross_correlation_ratio"
    }

    field = field_map.get(product, "reflectivity")

    display.plot(field, ax=ax)

    output_path = f"static/radar.png"
    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)

    return output_path
