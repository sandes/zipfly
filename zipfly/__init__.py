# -*- coding: utf-8 -*-
"""
Iterable ZIP archive generator.

Derived directly from zipfile.py
"""
from __future__ import unicode_literals, print_function, with_statement

__version__ = '1.0.0'

import os
import sys
import stat
import struct
import time
import zipfile

from .compat import (
    str, bytes,
    ZIP64_VERSION,
    ZIP_BZIP2, BZIP2_VERSION,
    ZIP_LZMA, LZMA_VERSION,
    SEEK_SET, SEEK_CUR, SEEK_END)

from zipfile import (
    ZIP_STORED, ZIP64_LIMIT, ZIP_FILECOUNT_LIMIT, ZIP_MAX_COMMENT,
    ZIP_DEFLATED,
    structCentralDir, structEndArchive64, structEndArchive, structEndArchive64Locator,
    stringCentralDir, stringEndArchive64, stringEndArchive, stringEndArchive64Locator,
    structFileHeader, stringFileHeader,
    zlib, crc32)

stringDataDescriptor = b'PK\x07\x08'  # magic number for data descriptor


def _get_compressor(compress_type):
    if compress_type == ZIP_DEFLATED:
        return zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
    elif compress_type == ZIP_BZIP2:
        from zipfile import bz2
        return bz2.BZ2Compressor()
    elif compress_type == ZIP_LZMA:
        from zipfile import LZMACompressor
        return LZMACompressor()
    else:
        return None


class PointerIO(object):
    def __init__(self, mode='wb'):
        if mode not in ('wb', ):
            raise RuntimeError('zipfly.ZipFile() requires mode "wb"')
        self.data_pointer = 0
        self.__mode = mode
        self.__closed = False

    @property
    def mode(self):
        return self.__mode

    @property
    def closed(self):
        return self.__closed

    def close(self):
        self.__closed = True

    def flush(self):
        pass

    def next(self):
        raise NotImplementedError()

    # def seek(self, offset, whence=None):
    #     if whence == SEEK_SET:
    #         if offset < 0:
    #             raise ValueError('negative seek value -1')
    #         self.data_pointer = offset
    #     elif whence == SEEK_CUR:
    #         self.data_pointer = max(0, self.data_pointer + offset)
    #     elif whence == SEEK_END:
    #         self.data_pointer = max(0, offset)
    #     return self.data_pointer

    def tell(self):
        return self.data_pointer

    def truncate(size=None):
        raise NotImplementedError()

    def write(self, data):
        if self.closed:
            raise ValueError('I/O operation on closed file')

        if isinstance(data, str):
            data = data.encode('utf-8')
        if not isinstance(data, bytes):
            raise TypeError('expected bytes')
        self.data_pointer += len(data)
        return data


class ZipInfo(zipfile.ZipInfo):
    def __init__(self, *args, **kwargs):
        zipfile.ZipInfo.__init__(self, *args, **kwargs)
        self.flag_bits = 0x08           # ZIP flag bits, bit 3 indicates presence of data descriptor

    def FileHeader(self, zip64=None):
        """Return the per-file header as a string."""
        dt = self.date_time
        dosdate = (dt[0] - 1980) << 9 | dt[1] << 5 | dt[2]
        dostime = dt[3] << 11 | dt[4] << 5 | (dt[5] // 2)
        if self.flag_bits & 0x08:
            # Set these to zero because we write them after the file data
            CRC = compress_size = file_size = 0
        else:
            CRC = self.CRC
            compress_size = self.compress_size
            file_size = self.file_size

        extra = self.extra

        min_version = 0
        if zip64 is None:
            zip64 = file_size > ZIP64_LIMIT or compress_size > ZIP64_LIMIT
        if zip64:
            fmt = b'<HHQQ'
            extra = extra + struct.pack(fmt,
                    1, struct.calcsize(fmt)-4, file_size, compress_size)
        if file_size > ZIP64_LIMIT or compress_size > ZIP64_LIMIT:
            if not zip64:
                raise LargeZipFile("Filesize would require ZIP64 extensions")
            # File is larger than what fits into a 4 byte integer,
            # fall back to the ZIP64 extension
            file_size = 0xffffffff
            compress_size = 0xffffffff
            min_version = ZIP64_VERSION

        if self.compress_type == ZIP_BZIP2:
            min_version = max(BZIP2_VERSION, min_version)
        elif self.compress_type == ZIP_LZMA:
            min_version = max(LZMA_VERSION, min_version)

        self.extract_version = max(min_version, self.extract_version)
        self.create_version = max(min_version, self.create_version)
        filename, flag_bits = self._encodeFilenameFlags()
        header = struct.pack(structFileHeader, stringFileHeader,
                 self.extract_version, self.reserved, flag_bits,
                 self.compress_type, dostime, dosdate, CRC,
                 compress_size, file_size,
                 len(filename), len(extra))
        return header + filename + extra

    def DataDescriptor(self):
        """
        crc-32                          4 bytes
        compressed size                 4 bytes
        uncompressed size               4 bytes
        """
        if self.compress_size > ZIP64_LIMIT or self.file_size > ZIP64_LIMIT:
            fmt = b'<4sLQQ'
        else:
            fmt = b'<4sLLL'
        return struct.pack(fmt, stringDataDescriptor, self.CRC, self.compress_size, self.file_size)


class ZipFile(zipfile.ZipFile):
    def __init__(self, fileobj=None, mode='w', compression=ZIP_STORED, allowZip64=False):
        """Open the ZIP file with mode write "w"."""
        if mode not in ('w', ):
            raise RuntimeError('zipfly.ZipFile() requires mode "w"')
        if fileobj is None:
            fileobj = PointerIO()

        self._comment = b''
        zipfile.ZipFile.__init__(self, fileobj, mode=mode, compression=compression, allowZip64=allowZip64)
        # TODO: Refractor to write queue with args + kwargs matching write()
        self.paths_to_write = []

    def __iter__(self):
        for kwargs in self.paths_to_write:
            for data in self.__write(**kwargs):
                yield data
        for data in self.__close():
            yield data

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    @property
    def comment(self):
        """The comment text associated with the ZIP file."""
        return self._comment

    @comment.setter
    def comment(self, comment):
        if not isinstance(comment, bytes):
            raise TypeError("comment: expected bytes, got %s" % type(comment))
        # check for valid comment length
        if len(comment) >= ZIP_MAX_COMMENT:
            if self.debug:
                print('Archive comment is too long; truncating to %d bytes'
                        % ZIP_MAX_COMMENT)
            comment = comment[:ZIP_MAX_COMMENT]
        self._comment = comment
        self._didModify = True

    def write(self, filename, arcname=None, compress_type=None):
        # TODO: Reflect python's Zipfile.write
        #   - if filename is file, write as file
        #   - if filename is directory, write an empty directory
        kwargs = {'filename': filename, 'arcname': arcname, 'compress_type': compress_type}
        self.paths_to_write.append(kwargs)

    def write_iter(self, arcname, iterable, compress_type=None):
        """Write the bytes iterable `iterable` to the archive under the name `arcname`."""
        kwargs = {'arcname': arcname, 'iterable': iterable, 'compress_type': compress_type}
        self.paths_to_write.append(kwargs)

    def writestr(self, arcname, data, compress_type=None):
        """
        Writes a str into ZipFile by wrapping data as a generator
        """
        def _iterable():
            yield data
        return self.write_iter(arcname, _iterable(), compress_type=compress_type)

    def __write(self, filename=None, iterable=None, arcname=None, compress_type=None):
        """Put the bytes from filename into the archive under the name
        `arcname`."""
        if not self.fp:
            raise RuntimeError(
                  "Attempt to write to ZIP archive that was already closed")
        if (filename is None and iterable is None) or (filename is not None and iterable is not None):
            raise ValueError("either (exclusively) filename or iterable shall be not None")

        if filename:
            st = os.stat(filename)
            isdir = stat.S_ISDIR(st.st_mode)
            mtime = time.localtime(st.st_mtime)
            date_time = mtime[0:6]
        else:
            st, isdir, date_time = None, False, time.localtime()[0:6]
        # Create ZipInfo instance to store file information
        if arcname is None:
            arcname = filename
        arcname = os.path.normpath(os.path.splitdrive(arcname)[1])
        while arcname[0] in (os.sep, os.altsep):
            arcname = arcname[1:]
        if isdir:
            arcname += '/'
        zinfo = ZipInfo(arcname, date_time)
        if st:
            zinfo.external_attr = (st[0] & 0xFFFF) << 16      # Unix attributes
        else:
            zinfo.external_attr = 0o600 << 16     # ?rw-------
        if compress_type is None:
            zinfo.compress_type = self.compression
        else:
            zinfo.compress_type = compress_type

        if st:
            zinfo.file_size = st[6]
        else:
            zinfo.file_size = 0
        zinfo.flag_bits = 0x00
        zinfo.flag_bits |= 0x08                 # ZIP flag bits, bit 3 indicates presence of data descriptor
        zinfo.header_offset = self.fp.tell()    # Start of header bytes
        if zinfo.compress_type == ZIP_LZMA:
            # Compressed data includes an end-of-stream (EOS) marker
            zinfo.flag_bits |= 0x02

        self._writecheck(zinfo)
        self._didModify = True

        if isdir:
            zinfo.file_size = 0
            zinfo.compress_size = 0
            zinfo.CRC = 0
            self.filelist.append(zinfo)
            self.NameToInfo[zinfo.filename] = zinfo
            yield self.fp.write(zinfo.FileHeader(False))
            return

        cmpr = _get_compressor(zinfo.compress_type)

        # Must overwrite CRC and sizes with correct data later
        zinfo.CRC = CRC = 0
        zinfo.compress_size = compress_size = 0
        # Compressed size can be larger than uncompressed size
        zip64 = self._allowZip64 and \
                zinfo.file_size * 1.05 > ZIP64_LIMIT
        yield self.fp.write(zinfo.FileHeader(zip64))
        file_size = 0
        if filename:
            with open(filename, 'rb') as fp:
                while 1:
                    buf = fp.read(1024 * 8)
                    if not buf:
                        break
                    file_size = file_size + len(buf)
                    CRC = crc32(buf, CRC) & 0xffffffff
                    if cmpr:
                        buf = cmpr.compress(buf)
                        compress_size = compress_size + len(buf)
                    yield self.fp.write(buf)
        else: # we have an iterable
            for buf in iterable:
                file_size = file_size + len(buf)
                CRC = crc32(buf, CRC) & 0xffffffff
                if cmpr:
                    buf = cmpr.compress(buf)
                    compress_size = compress_size + len(buf)
                yield self.fp.write(buf)
        if cmpr:
            buf = cmpr.flush()
            compress_size = compress_size + len(buf)
            yield self.fp.write(buf)
            zinfo.compress_size = compress_size
        else:
            zinfo.compress_size = file_size
        zinfo.CRC = CRC
        zinfo.file_size = file_size
        if not zip64 and self._allowZip64:
            if file_size > ZIP64_LIMIT:
                raise RuntimeError('File size has increased during compressing')
            if compress_size > ZIP64_LIMIT:
                raise RuntimeError('Compressed size larger than uncompressed size')

        # Seek backwards and write file header (which will now include
        # correct CRC and file sizes)
        # position = self.fp.tell()       # Preserve current position in file
        # self.fp.seek(zinfo.header_offset, 0)
        # self.fp.write(zinfo.FileHeader(zip64))
        # self.fp.seek(position, 0)
        yield self.fp.write(zinfo.DataDescriptor())
        self.filelist.append(zinfo)
        self.NameToInfo[zinfo.filename] = zinfo

    def __close(self):
        """Close the file, and for mode "w" write the ending
        records."""
        if self.fp is None:
            return

        try:
            if self.mode in ('w', 'a') and self._didModify:  # write ending records
                count = 0
                pos1 = self.fp.tell()
                for zinfo in self.filelist:         # write central directory
                    count = count + 1
                    dt = zinfo.date_time
                    dosdate = (dt[0] - 1980) << 9 | dt[1] << 5 | dt[2]
                    dostime = dt[3] << 11 | dt[4] << 5 | (dt[5] // 2)
                    extra = []
                    if zinfo.file_size > ZIP64_LIMIT \
                            or zinfo.compress_size > ZIP64_LIMIT:
                        extra.append(zinfo.file_size)
                        extra.append(zinfo.compress_size)
                        file_size = 0xffffffff
                        compress_size = 0xffffffff
                    else:
                        file_size = zinfo.file_size
                        compress_size = zinfo.compress_size

                    if zinfo.header_offset > ZIP64_LIMIT:
                        extra.append(zinfo.header_offset)
                        header_offset = 0xffffffff
                    else:
                        header_offset = zinfo.header_offset

                    extra_data = zinfo.extra
                    min_version = 0
                    if extra:
                        # Append a ZIP64 field to the extra's
                        extra_data = struct.pack(
                                b'<HH' + b'Q'*len(extra),
                                1, 8*len(extra), *extra) + extra_data
                        min_version = ZIP64_VERSION

                    if zinfo.compress_type == ZIP_BZIP2:
                        min_version = max(BZIP2_VERSION, min_version)
                    elif zinfo.compress_type == ZIP_LZMA:
                        min_version = max(LZMA_VERSION, min_version)

                    extract_version = max(min_version, zinfo.extract_version)
                    create_version = max(min_version, zinfo.create_version)
                    try:
                        filename, flag_bits = zinfo._encodeFilenameFlags()
                        centdir = struct.pack(structCentralDir,
                            stringCentralDir, create_version,
                            zinfo.create_system, extract_version, zinfo.reserved,
                            flag_bits, zinfo.compress_type, dostime, dosdate,
                            zinfo.CRC, compress_size, file_size,
                            len(filename), len(extra_data), len(zinfo.comment),
                            0, zinfo.internal_attr, zinfo.external_attr,
                            header_offset)
                    except DeprecationWarning:
                        print((structCentralDir, stringCentralDir, create_version,
                            zinfo.create_system, extract_version, zinfo.reserved,
                            zinfo.flag_bits, zinfo.compress_type, dostime, dosdate,
                            zinfo.CRC, compress_size, file_size,
                            len(zinfo.filename), len(extra_data), len(zinfo.comment),
                            0, zinfo.internal_attr, zinfo.external_attr,
                            header_offset), file=sys.stderr)
                        raise
                    yield self.fp.write(centdir)
                    yield self.fp.write(filename)
                    yield self.fp.write(extra_data)
                    yield self.fp.write(zinfo.comment)

                pos2 = self.fp.tell()
                # Write end-of-zip-archive record
                centDirCount = count
                centDirSize = pos2 - pos1
                centDirOffset = pos1
                if (centDirCount >= ZIP_FILECOUNT_LIMIT or
                    centDirOffset > ZIP64_LIMIT or
                    centDirSize > ZIP64_LIMIT):
                    # Need to write the ZIP64 end-of-archive records
                    zip64endrec = struct.pack(
                            structEndArchive64, stringEndArchive64,
                            44, 45, 45, 0, 0, centDirCount, centDirCount,
                            centDirSize, centDirOffset)
                    yield self.fp.write(zip64endrec)

                    zip64locrec = struct.pack(
                            structEndArchive64Locator,
                            stringEndArchive64Locator, 0, pos2, 1)
                    yield self.fp.write(zip64locrec)
                    centDirCount = min(centDirCount, 0xFFFF)
                    centDirSize = min(centDirSize, 0xFFFFFFFF)
                    centDirOffset = min(centDirOffset, 0xFFFFFFFF)

                endrec = struct.pack(structEndArchive, stringEndArchive,
                                    0, 0, centDirCount, centDirCount,
                                    centDirSize, centDirOffset, len(self._comment))
                yield self.fp.write(endrec)
                yield self.fp.write(self._comment)
                self.fp.flush()
        finally:
            fp = self.fp
            self.fp = None
            if not self._filePassed:
                fp.close()
