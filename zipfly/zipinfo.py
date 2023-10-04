import os
import zipfile

from datetime import datetime


class CloudZipInfo(zipfile.ZipInfo):
    @classmethod
    def from_file(cls, filename, arcname=None, isdir=None, date_time=None, st_mode=None, st_size=None, strict_timestamps=True):
        """Construct an appropriate ZipInfo for a file on the filesystem.

        filename should be the path to a file or directory on the filesystem.

        arcname is the name which it will have within the archive (by default,
        this will be the same as filename, but without a drive letter and with
        leading path separators removed).
        """
        if isinstance(filename, os.PathLike):
            filename = os.fspath(filename)

        if isdir is None:
            if str(filename).endswith(os.sep):
                isdir = True
            else:
                isdir = False

        if date_time is None:
            date_time = datetime.now().timetuple()[:6]
        if not strict_timestamps and date_time[0] < 1980:
            date_time = (1980, 1, 1, 0, 0, 0)
        elif not strict_timestamps and date_time[0] > 2107:
            date_time = (2107, 12, 31, 23, 59, 59)

        # Create ZipInfo instance to store file information
        if arcname is None:
            arcname = filename
        arcname = arcname.split("://")[-1] # For cloud. This must be before normalize
        arcname = os.path.normpath(os.path.splitdrive(arcname)[1])
        while arcname[0] in (os.sep, os.altsep):
            arcname = arcname[1:]
        if isdir and arcname[-1] != '/':
            arcname += '/'
        zinfo = cls(arcname, date_time)

        if st_mode is None:
            if isdir:
                st_mode = 16877
            else:
                st_mode = 33188
        zinfo.external_attr = (st_mode & 0xFFFF) << 16  # Unix attributes

        if isdir:
            zinfo.file_size = 0
            zinfo.external_attr |= 0x10  # MS-DOS directory flag
        else:
            if st_size is None:
                raise ValueError("st_size must not be None for files")
            zinfo.file_size = st_size

        return zinfo
