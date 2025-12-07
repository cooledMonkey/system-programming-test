import os
import queue
import threading

from flask import Flask, jsonify, request

app = Flask(__name__)


def get_str_count(file_name):
    with open(file_name, 'rb') as f:
        count = sum(1 for _ in f)
    return count


def analyze_file_threading(file_name):
    return get_str_count(file_name)


def worker(file_queue, result_queue):
    while True:
        try:
            file_path = file_queue.get_nowait()
        except queue.Empty:
            break
        result_queue.put(analyze_file_threading(file_path))
        file_queue.task_done()


@app.route('/')
def handler():
    files = []
    dir_name = request.args.get('dir_name')
    file_queue = queue.Queue()
    result_queue = queue.Queue()
    directory = os.fsencode(dir_name)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            files.append(dir_name + "/" + filename)
    for file_path in files:
        file_queue.put(file_path)
    num_threads = min(8, len(files))
    thread_list = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(file_queue, result_queue))
        t.start()
        thread_list.append(t)
    file_queue.join()
    for i in thread_list:
        i.join()
    response = 0
    for i in range(len(thread_list)):
        response += result_queue.get()
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, threaded=True)
