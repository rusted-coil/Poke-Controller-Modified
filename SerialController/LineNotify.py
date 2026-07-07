import configparser
import cv2
import io
import os

import requests
from PIL import Image
from logging import getLogger, DEBUG, NullHandler


class Line_Notify:

    def __init__(self, camera=None, token_name='token'):
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.res = None
        self.token_file = configparser.ConfigParser(comment_prefixes='#', allow_no_value=True)
        self.open_file_with_utf8()
        self.camera = camera
        self.token_list = {key: self.token_file['LINE'][key] for key in self.token_file['LINE']}
        self.token_num = len(self.token_list)
        # self.line_notify_token = self.token_file['LINE'][token_name]
        self.headers = [{'Authorization': f'Bearer {token}'} for key, token in self.token_list.items()]
        self.res = [requests.get('https://notify-api.line.me/api/status', headers=head) for head in self.headers]
        self.status = [responses.status_code for responses in self.res]
        self.chk_token_json = [responses.json() for responses in self.res]

    def open_file_with_utf8(self):
        """
        Automatically detect if a UTF-8 file has BOM and load it
        """
        line_token_path = os.path.join(os.path.dirname(__file__), 'line_token.ini')
        is_with_bom = self.is_utf8_file_with_bom(line_token_path)

        encoding = 'utf-8-sig' if is_with_bom else 'utf-8'

        self._logger.debug("Load token file")
        self.token_file.read(line_token_path, encoding)

    def is_utf8_file_with_bom(self, filename):
        """
        Determine if a UTF-8 file has BOM
        """
        line_first = open(filename, encoding='utf-8').readline()
        return line_first[0] == '\ufeff'

    def __str__(self):
        for stat in self.status:
            if stat == 401:
                self._logger.error("Invalid token")
                return "LINE Token Check FAILED."
            elif stat == 200:
                self._logger.info("Valid token")
                return "LINE-Token Check OK!"

    def send_text(self, notification_message, token='token'):
        """
        Send text notification to LINE
        """
        line_notify_api = 'https://notify-api.line.me/api/notify'
        try:
            headers = {'Authorization': f'Bearer {self.token_list[token]}'}
            data = {'Message': f'{notification_message}'}
            self.res = requests.post(line_notify_api, headers=headers, data=data)
            if self.res.status_code == 200:
                print("[LINE]Text sent.")
                self._logger.info("Send text")
            else:
                print("[LINE]Failed to send text.")
                self._logger.error("Failed to send text")
        except KeyError:
            print('Incorrect token name')
            self._logger.error('Using the wrong token')

    def send_text_n_image(self, notification_message, token='token'):
        """
        Notify only text when camera is not open,
        and notify text and image when open
        """
        try:
            if self.camera is None:
                print("Camera is not Opened. Send text only.")
                self.send_text(notification_message)
                return

            image_bgr = self.camera.readFrame()
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image_rgb)
            png = io.BytesIO()  # Create an empty io.BytesIO object
            image.save(png, format='png')  # Write PNG file to the empty io.BytesIO object
            b_frame = png.getvalue()  # Read io.BytesIO object as bytes

            line_notify_api = 'https://notify-api.line.me/api/notify'
            headers = {'Authorization': f'Bearer {self.token_list[token]}'}
            data = {'Message': f'{notification_message}'}
            files = {'imageFile': b_frame}
            self.res = requests.post(line_notify_api, headers=headers, params=data, files=files)
            if self.res.status_code == 200:
                print("[LINE]Text and image sent.")
                self._logger.info("Send image with text")
            else:
                print("[LINE]Failed to send text and image.")
                self._logger.error("Failed to send image with text")
        except KeyError:
            print('Incorrect token name')
            self._logger.error('Using the wrong token')

    def getRateLimit(self):
        try:
            for i in range(self.token_num):
                print(f'For: {list(self.token_list.keys())[i]}')
                print('X-RateLimit-Limit: ' + self.res[i].headers['X-RateLimit-Limit'])
                print('X-RateLimit-ImageLimit: ' + self.res[i].headers['X-RateLimit-ImageLimit'])
                print('X-RateLimit-Remaining: ' + self.res[i].headers['X-RateLimit-Remaining'])
                print('X-RateLimit-ImageRemaining: ' + self.res[i].headers['X-RateLimit-ImageRemaining'])
                import datetime
                dt = datetime.datetime.fromtimestamp(int(self.res[i].headers['X-RateLimit-Reset']),
                                                     datetime.timezone(datetime.timedelta(hours=9)))
                print('Reset time:', dt, '\n')

                self._logger.info(f"LINE API - Limit: {self.res[i].headers['X-RateLimit-Limit']}")
                self._logger.info(f"LINE API - Remaining: {self.res[i].headers['X-RateLimit-Remaining']}")
                self._logger.info(f"LINE API - ImageLimit: {self.res[i].headers['X-RateLimit-Limit']}")
                self._logger.info(f"LINE API - ImageRemaining: {self.res[i].headers['X-RateLimit-ImageRemaining']}")
                self._logger.info(f"Reset time: {dt}")
        except AttributeError as e:
            self._logger.error(e)
            pass
        except KeyError as e:
            self._logger.error(e)
            pass


if __name__ == "__main__":
    '''
    status  HTTP status code compliant value
       200  On success
       401  Invalid access token
    '''
    LINE = Line_Notify()
    print(LINE)
    LINE.getRateLimit()
