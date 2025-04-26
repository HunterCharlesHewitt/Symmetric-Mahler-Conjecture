import csv
import json
from datetime import datetime


class FileWriterService:
    def __init__(self, delimiter=','):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"Results/output_{timestamp}.csv"
        self.delimiter = delimiter
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['ratio', 'T normal vectors', 'K normal vectors', 'C_K(T)', "Volume K Metric"])

    def write_billiard_system_to_file(self, bs):
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter, quoting=csv.QUOTE_MINIMAL)
            t_vs = bs.T.normal_vectors.tolist()
            k_vs = bs.K.normal_vectors.tolist()
            writer.writerow([bs.ratio,  json.dumps(t_vs),  json.dumps(k_vs), bs.capacity_k_of_t.length, bs.volume_k_metric])
