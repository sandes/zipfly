import io

class ZipflyStream( io.RawIOBase ):

    """
    The RawIOBase ABC extends IOBase. It deals with
    the reading and writing of bytes to a stream. FileIO subclasses
    RawIOBase to provide an interface to files in the machine’s file system.
    """

    def __init__(self):
        self._buffer = b''
        self._size = 0

    def writable(self):
        return True

    def write(self, b):
        if self.closed:
            raise RuntimeError("ZipFly stream was closed!")
        self._buffer += b
        return len(b)

    def get(self):
        chunk = self._buffer
        self._buffer = b''
        self._size += len(chunk)
        return chunk

    def size(self):
        return self._size
