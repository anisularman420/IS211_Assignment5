import requests
import csv

class Request:
    def __init__(self, timestamp, url, processing_time):
        self.timestamp = timestamp
        self.url = url
        self.processing_time = processing_time

class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def is_busy(self):
        return self.current_request is not None

    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.processing_time

    def tick(self):
        if self.current_request is not None:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_request = None

def simulate_one_server(input_url):
    response = requests.get(input_url)
    
    if response.status_code != 200:
        print("Failed to download the CSV file.")
        return

    request_list = []

    csv_content = response.text.splitlines()
    csv_reader = csv.reader(csv_content)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        timestamp, url, processing_time = row
        request = Request(int(timestamp), url, int(processing_time))
        request_list.append(request)

    server = Server()
    total_wait_time = 0

    for request in request_list:
        if server.is_busy():
            total_wait_time += server.time_remaining
            server.tick()
        server.start_next(request)
        total_wait_time += server.time_remaining
        server.tick()

    average_wait_time = total_wait_time / len(request_list)
    return average_wait_time

if __name__ == "__main__":
    input_url = "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"
    average_latency_single_server = simulate_one_server(input_url)
    print(f"Average latency for single server: {average_latency_single_server:.2f} seconds")
