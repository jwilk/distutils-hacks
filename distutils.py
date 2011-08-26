#!/usr/bin/python
# encoding=UTF-8

# Copyright © 2011 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Make tarballs generated by distutils anonymous:
- all files and directories owned by root:root;
- all directories with mode 0755;
- all files with mode 0644 or 0755.
'''

import os
import stat
import sys
import tarfile

sys_path0 = sys.path.pop(0)
me = sys.modules['distutils']
del sys.modules['distutils']
import distutils
sys.modules['distutils'] = distutils
sys.path[:0] = [sys_path0]

if sys.version_info >= (3, 0) and sys.version_info < (3, 2):

    raise NotImplementedError

if sys.version_info < (2, 7):

    # Before Python 2.7, distutils just called the tar(1) binary,
    # so the TAR_OPTIONS environment variable can be used.
    os.putenv('TAR_OPTIONS', '--owner root --group root --mode a+rX')

else:

    # In Python 2.7, distutils use the tarfile module. Let's monkey-patch it.

    original_add = tarfile.TarFile.add

    def root_filter(tarinfo):
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = 'root'
        tarinfo.mode |= 292 | ((tarinfo.mode & 64) and 73)
        return tarinfo

    def add(self, name, arcname=None, recursive=True, exclude=None, filter=None):
        return original_add(self,
            name=name,
            arcname=arcname,
            recursive=recursive,
            exclude=exclude,
            filter=root_filter
        )

    tarfile.TarFile.add = add

__all__ = []

# vim:ts=4 sw=4 et
