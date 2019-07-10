import unittest
import subprocess
import http.client
import os

personal_path = r"C:\Python230\lesson03\Russ_Github_versions\socket-http-server\webroot"
pp_images = r"C:\Python230\lesson03\Russ_Github_versions\socket-http-server\webroot\images"

class WebTestCase(unittest.TestCase):
    """tests for the echo server and client"""

    def setUp(self):
        self.server_process = subprocess.Popen(
            [
                "python",
                "http_server.py"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def tearDown(self):
        self.server_process.kill()
        self.server_process.communicate()

    def get_response(self, url):
        """
        Helper function to get a response from a given url, using http.client
        """

        conn = http.client.HTTPConnection('localhost:10000')
        conn.request('GET', url)

        response = conn.getresponse()

        conn.close()

        return response

    def test_post_yields_method_not_allowed(self):
        """
        Sending a POST request should yield a 405 Method Not Allowed response
        """

        conn = http.client.HTTPConnection('localhost:10000')
        conn.request('POST', '/')

        response = conn.getresponse()

        conn.close()

        self.assertEqual(response.getcode(), 405)


    def test_get_sample_text_content(self):
        """
        A call to /sample.txt returns the correct body
        """
        file = 'sample.txt'
        local_path = os.path.join(personal_path, file)
        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)

        with open(local_path, 'rb') as f:
            self.assertEqual(f.read(), response.read(), error_comment)

    def test_get_sample_text_mime_type(self):
        """
        A call to /sample.txt returns the correct mimetype
        """
        file = 'sample.txt'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)
        self.assertEqual(response.getheader('Content-Type'), 'text/plain', error_comment)

    def test_get_sample_scene_balls_jpeg(self):
        """
        A call to /images/Sample_Scene_Balls.jpg returns the correct body
        """
        file = 'Sample_Scene_Balls.jpg'

        webroot = pp_images
        local_path = os.path.join(webroot, file)
        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)

        with open(local_path, 'rb') as f:
            self.assertEqual(f.read(), response.read(), error_comment)

    def test_get_sample_scene_balls_jpeg_mime_type(self):
        """
        A call to /images/Sample_Scene_Balls.jpg returns the correct mimetype
        """
        file = 'Sample_Scene_Balls.jpg'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)
        self.assertEqual(response.getheader('Content-Type'), 'image/jpg', error_comment)

    def test_get_sample_1_png(self):
        """
        A call to /images/sample_1.png returns the correct body
        """
        file = 'sample_1.png'

        webroot = pp_images
        local_path = os.path.join(webroot, file)
        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)

        with open(local_path, 'rb') as f:
            self.assertEqual(f.read(), response.read(), error_comment)

    def test_get_sample_1_png_mime_type(self):
        """
        A call to /images/sample_1.png returns the correct mimetype
        """
        file = 'sample_1.png'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)
        self.assertEqual(response.getheader('Content-Type'), 'image/png', error_comment)

    def test_get_404(self):
        """
        A call to /asdf.txt (a file which does not exist in webroot) yields a 404 error
        """
        file = 'asdf.txt'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 404)

    def test_images_index(self):
        """
        A call to /images/ yields a list of files in the images directory
        """

        directory = 'images'
        local_path = os.path.join(personal_path, directory)
        web_path = '/' + directory
        error_comment = "Error encountered while visiting " + web_path

        test_list_count = 0
        test_list = 'JPEG_example.jpg', 'sample_1.png',\
                'Sample_Scene_Balls.jpg'

        for item in test_list:
            test_list_count += 1

        os_count = 0
        for path in os.listdir(local_path):
            os_count += 1

        self.assertEqual(test_list_count, os_count)

    def test_ok_response_at_root_index(self):
        """
        A call to / at least yields a 200 OK response
        """

        directory = ''
        web_path = '/' + directory

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200)