#!/usr/bin/env python3

# Copyright (c) 2009, David Buxton <david@gasmark6.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Tools to convert between Python datetime instances and Microsoft times.
"""
from datetime import datetime, timedelta, tzinfo
from calendar import timegm


# http://support.microsoft.com/kb/167296
# How To Convert a UNIX time_t to a Win32 FILETIME or SYSTEMTIME
EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
HUNDREDS_OF_NANOSECONDS = 10000000


ZERO = timedelta(0)
HOUR = timedelta(hours=1)


class UTC(tzinfo):
        """UTC"""
        def utcoffset(self, dt):
                return ZERO

        def tzname(self, dt):
                return "UTC"

        def dst(self, dt):
                return ZERO


utc = UTC()


def dt_to_filetime(dt):
        """Converts a datetime to Microsoft filetime format. If the object is
        time zone-naive, it is forced to UTC before conversion.

        >>> "%.0f" % dt_to_filetime(datetime(2009, 7, 25, 23, 0))
        '128930364000000000'

        >>> "%.0f" % dt_to_filetime(datetime(1970, 1, 1, 0, 0, tzinfo=utc))
        '116444736000000000'

        >>> "%.0f" % dt_to_filetime(datetime(1970, 1, 1, 0, 0))
        '116444736000000000'

        >>> dt_to_filetime(datetime(2009, 7, 25, 23, 0, 0, 100))
        128930364000001000
        """
        if (dt.tzinfo is None) or (dt.tzinfo.utcoffset(dt) is None):
                dt = dt.replace(tzinfo=utc)
        ft = EPOCH_AS_FILETIME + (timegm(dt.timetuple()) * HUNDREDS_OF_NANOSECONDS)
        return ft + (dt.microsecond * 10)


def filetime_to_dt(ft):
        """Converts a Microsoft filetime number to a Python datetime. The new
        datetime object is time zone-naive but is equivalent to tzinfo=utc.

        >>> filetime_to_dt(116444736000000000)
        datetime.datetime(1970, 1, 1, 0, 0)

        >>> filetime_to_dt(128930364000000000)
        datetime.datetime(2009, 7, 25, 23, 0)

        >>> filetime_to_dt(128930364000001000)
        datetime.datetime(2009, 7, 25, 23, 0, 0, 100)
        """
        # Get seconds and remainder in terms of Unix epoch
        (s, ns100) = divmod(ft - EPOCH_AS_FILETIME, HUNDREDS_OF_NANOSECONDS)
        # Convert to datetime object
        dt = datetime.utcfromtimestamp(s)
        # Add remainder in as microseconds. Python 3.2 requires an integer
        dt = dt.replace(microsecond=(ns100 // 10))
        return dt


if __name__ == "__main__":
        import doctest

        doctest.testmod()
