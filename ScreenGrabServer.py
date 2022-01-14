from socket import socket
from threading import Thread
from zlib import compress
from mss import mss

WIDTH = 1900
HEIGHT = 1000


def retrieve_screenshott(conn):
    with mss() as sct:
        #The region to capture
        rect = {'top':0, 'left':0, 'width':WIDTH, 'height':HEIGHT}

        while 'recording':
            #Capture the screen
            img = sct.grab(rect)
            pixels = compress(img.rgb, 6)

            #Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(byters([size_len]))

            #Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            #Send pixels
            conn.sendall(pixels)

def main(host='0.0.0.0', port=9999):
    sock = socket()
    sock.connect((host, port))
    try:
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=retrieve_screenshot, args=(conn,))
            thead.start()
        finally:
            sock.close()


if __name__ == '__main__':
    main()
