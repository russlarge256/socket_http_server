import socket
import sys
import traceback
import os
import array
from webroot import make_time

# In order to run this script successfully, please update the 'webroot'
# variable to the location of the 'webroot' folder on your machine.

webroot = r"C:\Python230\lesson03\Russ_Github_versions\socket-http-server\webroot"
images = os.path.join(webroot, "\images")


def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):

    # TODO: Implement response_ok
    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: " + mimetype,
        b"",
        body,
    ])


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    # TODO: Implement response_method_not_allowed

    return b"/r/n".join([
        b"HTTP/1.1 405 Method Not Allowed",
        b"",
        b"You can't do that on this server!"
    ])


def response_not_found():
    """Returns a 404 Not Found response"""

    # TODO: Implement response_not_found
    return b"/r/n".join([
        b"HTTP/1.1 404 Method Not Found",
        b"",
        b"You can't do that on this server!"
    ])


def parse_request(request):

    # TODO: implement parse_request
    method, path, version = request.split("\r\n")[0].split(" ")

    if method != "GET":
        raise NotImplementedError

    return path


def image_to_bytes(path):

    with open(path, "rb") as image:

        f = image.read()
        b = bytearray(f)

        return b


def response_path(path):

    # TODO: Raise a NameError if the requested content is not present
    # TODO: Fill in the appropriate content and mime_type give the path.

    p = path[1:]


    all_content = []
    itemized_list = [item for item in all_content]

    content = bytes(os.path.join(webroot, p), encoding="utf-8")
    mime_type = b"text/plain"

    if path == "/":
        # write dir items to in-memory file
        for item in os.listdir(webroot):
            with open("tst", "a") as f:
                f.write(item)
                f.write(',')
                f.write('\n')

        # read in-memory file
        with open("tst", "r", encoding="utf-8")as r:
            reader = r.read()

        # convert items to bytes and set as content for page
        content = bytes(reader, encoding="utf-8")

        # remove items from file (so data is not appended every time)
        with open("tst", "w") as rem:
            rem.write("")

        all_content.append(path)

    elif p == 'sample.txt':
        fullpath = os.path.join(webroot, p)
        with open(fullpath, 'rb') as file:
            reader = file.read()
        content = reader
        mime_type = b"text/plain"

    elif p == 'favicon.ico':
        content = image_to_bytes(os.path.join(webroot, p))
        mime_type = b"image/x-icon"

        all_content.append(p)

    elif p == 'make_time.py':
        content = bytes(make_time.show_time(), encoding="utf=8")
        mime_type = b"text/html"

        all_content.append(p)

    elif p.__contains__('sample_1.png'):
        content = image_to_bytes(os.path.join(webroot, "images", p))
        mime_type = b"image/png"

        all_content.append(p)

    elif p.__contains__('JPEG_example.jpg') or\
            p.__contains__('Sample_Scene_Balls.jpg'):
        content = image_to_bytes(os.path.join(webroot, "images", p))
        mime_type = b"image/jpg"

        all_content.append(p)

    elif p.__contains__('a_web_page.html'):
        fullpath = os.path.join(webroot, p)
        with open(fullpath, 'r', encoding="utf-8") as file:
            reader = file.read()
        content = bytes(reader, encoding='utf-8')
        mime_type = b"text/html"

        all_content.append(p)

    elif p.__contains__('images'):
        list = ""
        for item in images:
            with open(list, 'w') as ok:
                ok.write(item)

        content = bytes('all_images', encoding="utf-8")

        all_content.append(p)

    elif p != itemized_list:
        content = response_not_found()

    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break

                print("Request received:\n{}\n\n".format(request))

                try:
                    path = parse_request(request)

                    response = response_ok(
                        body=response_path(path)[0], mimetype=response_path(path)[1]
                    )

                except NotImplementedError:
                    response = response_method_not_allowed()

                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)


