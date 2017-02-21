#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import struct

from ansible.module_utils.basic import AnsibleModule


class XipArchive(object):
    def __init__(self, src="", dest="", module=None):
        self.src = src
        self.dest = dest
        self.module = module

    def extract(self):
        os.chdir(self.dest)
        archive_files = self._split_file(self.src)

        # there's only ever "Content" and "Metadata"
        xz_parts = self._unpack_pbxz_stream("Content")

        extraction = self._extract_xz_archive(xz_parts[0])

        if not extraction:
            self.module.fail_json("Failed to extract final part of archive.")

        for file_name in (archive_files + xz_parts):
            self.module.add_cleanup_file(file_name)

        self.module.do_cleanup_files()

    def _split_file(self, src):
        cmd = "xar -tf %s" % src
        rc, out, err = self.module.run_command(cmd, cwd=self.dest)

        stream_files = out.splitlines()
        # validate output files look right?

        cmd = "xar -xf %s" % src
        rc, out, err = self.module.run_command(cmd, cwd=self.dest)

        return stream_files

    def _unpack_pbxz_stream(self, file_name):
        file_name = os.path.abspath(file_name)

        parts = []
        section = 0
        xar_out_path = '%s.part%02d.cpio.xz' % (file_name, section)
        parts.append(xar_out_path)

        f = open(file_name, 'rb')
        magic = self._seekread(f, length=4)
        if magic != 'pbzx':
            raise "Error: Not a pbzx file"

        # Read 8 bytes for initial flags
        flags = self._seekread(f, length=8)
        # Interpret the flags as a 64-bit big-endian unsigned int
        flags = struct.unpack('>Q', flags)[0]
        xar_f = open(xar_out_path, 'wb')

        while (flags & (1 << 24)):
            # Read in more flags
            flags = self._seekread(f, length=8)
            flags = struct.unpack('>Q', flags)[0]

            # Read in length
            f_length = self._seekread(f, length=8)
            f_length = struct.unpack('>Q', f_length)[0]
            xzmagic = self._seekread(f, length=6)

            if xzmagic != '\xfd7zXZ\x00':
                # This isn't xz content, this is actually
                # _raw decompressed cpio_ chunk of 16MB in size...
                # Let's back up ...
                self._seekread(f, offset=-6, length=0)
                # ... and split it out ...
                f_content = self._seekread(f, length=f_length)
                section += 1
                decomp_out = '%s.part%02d.cpio' % (file_name, section)
                g = open(decomp_out, 'wb')
                g.write(f_content)
                g.close()

                # Now to start the next section, which should hopefully be
                # .xz (we'll just assume it is ...)
                xar_f.close()
                section += 1
                new_out = '%s.part%02d.cpio.xz' % (file_name, section)
                parts.append(new_out)
                xar_f = open(new_out, 'wb')
            else:
                f_length -= 6
                # This part needs buffering
                f_content = self._seekread(f, length=f_length)
                tail = self._seekread(f, offset=-2, length=2)
                xar_f.write(xzmagic)
                xar_f.write(f_content)
                if tail != 'YZ':
                    xar_f.close()
                    raise "Error: Footer is not xar file footer"
        try:
            f.close()
            xar_f.close()
        except:
            pass

        return parts

    def _seekread(self, f, offset=None, length=0, relative=True):
        if offset is not None:
            # offset provided, let's seek
            f.seek(offset, [0, 1, 2][relative])
        if length is not 0:
            return f.read(length)

    def _extract_xz_archive(self, file_name):
        if not os.path.isfile(file_name):
            self.module.fail_json(
                msg="xz archive %s is not a file" % file_name)

        cmd = "cpio -izmdu 0<%s" % file_name
        rc, out, err = self.module.run_command(cmd, cwd=self.dest,
                                               use_unsafe_shell=True)

        return True if rc == 0 else False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(required=True, type="path"),
            dest=dict(required=True, type="path")
        )
    )

    src = os.path.expanduser(module.params["src"])
    dest = os.path.expanduser(module.params["dest"])

    if not os.path.exists(src):
        module.fail_json(msg="Source '%s' failed to transfer" % src)

    xip_archive = XipArchive(src, dest, module=module)
    xip_archive.extract()

    module.exit_json(changed=True)


if __name__ == "__main__":
    main()
