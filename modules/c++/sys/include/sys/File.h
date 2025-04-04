/* =========================================================================
 * This file is part of sys-c++
 * =========================================================================
 *
 * (C) Copyright 2004 - 2014, MDA Information Systems LLC
 *
 * sys-c++ is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; If not,
 * see <http://www.gnu.org/licenses/>.
 *
 */

#pragma once
#ifndef CODA_OSS_sys_File_h_INCLUDED_
#define CODA_OSS_sys_File_h_INCLUDED_

#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

#include <memory>
#include <fstream>

#include "sys/Conf.h"
#include "sys/SystemException.h"
#include "sys/Path.h"
#include "sys/filesystem.h"
#include "config/Exports.h"

#ifdef _WIN32
#    define _SYS_SEEK_CUR FILE_CURRENT
#    define _SYS_SEEK_SET FILE_BEGIN
#    define _SYS_SEEK_END FILE_END
#    define _SYS_CREAT    OPEN_ALWAYS
#    define _SYS_OPEN_EXISTING OPEN_EXISTING
#    define _SYS_TRUNC 8
#    define _SYS_RDONLY GENERIC_READ
#    define _SYS_WRONLY GENERIC_WRITE
#    define _SYS_RDWR GENERIC_READ|GENERIC_WRITE
#    define SYS_INVALID_HANDLE INVALID_HANDLE_VALUE
typedef HANDLE _SYS_HANDLE_TYPE;
#else
#    define _SYS_DEFAULT_PERM 0644
#    define _SYS_MAX_READ_ATTEMPTS 100
#    define _SYS_SEEK_CUR SEEK_CUR
#    define _SYS_SEEK_SET SEEK_SET
#    define _SYS_SEEK_END SEEK_END
#    define _SYS_CREAT O_CREAT
#    define _SYS_OPEN_EXISTING 0
#    define _SYS_TRUNC O_TRUNC
#    define _SYS_RDONLY O_RDONLY
#    define _SYS_WRONLY O_WRONLY
#    define _SYS_RDWR O_RDWR
#    define SYS_INVALID_HANDLE -1
typedef int _SYS_HANDLE_TYPE;
#endif

/*!
 *  \class File
 *  \brief Cross-platform API for file descriptor access
 *
 *  This API exists primarily as a wrapper for the system
 *  OS behavior.  It is intended that this class be capable
 *  of reading > 2GB files on all platforms.
 *
 */

namespace sys
{
struct CODA_OSS_API File
{
    enum
    {
        FROM_START = _SYS_SEEK_SET,
        FROM_CURRENT = _SYS_SEEK_CUR,
        FROM_END = _SYS_SEEK_END,
        CREATE = _SYS_CREAT,
        EXISTING = _SYS_OPEN_EXISTING,
        TRUNCATE = _SYS_TRUNC,
        READ_ONLY = _SYS_RDONLY,
        WRITE_ONLY = _SYS_WRONLY,
        READ_AND_WRITE = _SYS_RDWR
    };

    /*!
     *  Default constructor.  Does nothing
     */
    File() = default;

    /*!
     *  Constructor.  Initializes to a file.
     *  \param str A file name to open
     *  \param accessFlags File access flags
     *  \param creationFlags File creation flags
     */
    File(const Path& path,
         int accessFlags = READ_ONLY,
         int creationFlags = EXISTING)
    {
        create(path.getPath(), accessFlags, creationFlags);
    }
    File(std::nothrow_t, const coda_oss::filesystem::path& path,
         int accessFlags = READ_ONLY, int creationFlags = EXISTING) noexcept // caller MUST check isOpen()
    {
        create(std::nothrow, path, accessFlags, creationFlags);
    }

    File(const Path& parent, std::string name, int accessFlags = READ_ONLY,
         int creationFlags = EXISTING)
    {
        create(parent.join(name).getPath(), accessFlags, creationFlags);
    }
    File(std::nothrow_t, const coda_oss::filesystem::path& parent, const coda_oss::filesystem::path& name,
         int accessFlags = READ_ONLY, int creationFlags = EXISTING) noexcept // caller MUST check isOpen()
    {
        create(std::nothrow, parent / name, accessFlags, creationFlags);
    }

    /*!
     *  Constructor.  Initializes to a file.
     *  \param str A file name to open
     *  \param accessFlags File access flags
     *  \param creationFlags File creation flags
     */
    explicit File(const std::string& str,
                  int accessFlags = READ_ONLY,
                  int creationFlags = EXISTING)
    {
        create(str, accessFlags, creationFlags);
    }

    /*!
     *  Destructor.  Closes file if open.
     */
    ~File()
    {
        if (isOpen())
            close();
    }

    File(const File&) = default;
    File& operator=(const File&) = default;
    File(File&&) = default;
    File& operator=(File&&) = default;

    /*!
     *  Is the file open?
     *  \return true if open, false if invalid handle
     */
    bool isOpen() const noexcept
    {
        return (mHandle != SYS_INVALID_HANDLE);
    }

    /*!
     *  Return the underlying file handle
     *
     */
    _SYS_HANDLE_TYPE getHandle() noexcept
    {
        return mHandle;
    }

    sys::Path getPath() const
    {
        return sys::Path(mPath);
    }

    inline std::string getName() const
    {
        return getPath().split().second;
    }

    /*!
     *  Initialize the object to a file.
     *  \param str A file name to open
     *  \param accessFlags File access flags
     *  \param creationFlags File creation flags
     */
    void create(const std::string& str, int accessFlags, int creationFlags);
    void create(std::nothrow_t, const coda_oss::filesystem::path& path,
                           int accessFlags, int creationFlags) // caller MUST check isOpen()
    {
        mHandle = createFile(path, accessFlags, creationFlags);
        mPath = path.string();
    }

    /*!
     *  Read from the File into a buffer 'size' bytes.
     *  Blocks.
     *  If size is 0, no OS level read operation occurs.
     *  If size is < 0, an exception is thrown.
     *  If size is > length of file, an exception occurs.
     *
     *  \param buffer The buffer to put to
     *  \param size The number of bytes
     */
    void readInto(void* buffer, size_t size);

    /*!
     *  Read from the File, at offset bytes from the beginning, into a buffer
     *  'size' bytes.  Does not use but may update the internal file pointer.
     *  Blocks.
     *  If size is 0, no OS level read operation occurs.
     *  If size is < 0, an exception is thrown.
     *  If size is > length of file, an exception occurs.
     *
     *  \param buffer The buffer to put to
     *  \param size The number of bytes
     */
    void readAtInto(sys::Off_T offset, void* buffer, size_t size);

    /*!
     *  Write from a buffer 'size' bytes into the
     *  file.
     *  Blocks.
     *  If size is 0, no OS level write operation occurs.
     *  If size is < 0, an exception is thrown.
     *
     *  \param buffer The buffer to read from
     *  \param size The number of bytes to write out
     */
    void writeFrom(const void* buffer,
                   size_t size);

    /*!
     *  Seek to the specified offset, relative to 'whence.'
     *  Valid values are FROM_START, FROM_CURRENT, FROM_END.
     *
     *  \return Global offset location.
     */

    sys::Off_T seekTo(sys::Off_T offset, int whence);

    /*!
     *  Report current offset within file.
     *
     *  \return Current offset;
     */
    sys::Off_T getCurrentOffset()
    {
        return seekTo(0, sys::File::FROM_CURRENT);
    }

    /*!
     * Report the length of the file.
     * \return The length
     */
    sys::Off_T length();

    /*!
     * Returns the last modified time of the file, in millis.
     * \return last modified time
     */
    sys::Off_T lastModifiedTime();

    /*!
     *  Flush the file to disk
     */
    void flush();

    /*!
     *  Close the handle.
     */
    void close();

protected:
    _SYS_HANDLE_TYPE mHandle = SYS_INVALID_HANDLE;
    std::string mPath;

    static _SYS_HANDLE_TYPE createFile(const coda_oss::filesystem::path&, int accessFlags, int creationFlags) noexcept;

};

// These routines use sys::expandEnvironmentVariables() if the initial open attempt fails.
CODA_OSS_API File make_File(const coda_oss::filesystem::path&, int accessFlags = File::READ_ONLY, int creationFlags =  File::EXISTING);
CODA_OSS_API File make_File(const coda_oss::filesystem::path& parent, const coda_oss::filesystem::path& name,
        int accessFlags =  File::READ_ONLY, int creationFlags =  File::EXISTING);


// Call  sys::expandEnvironmentVariables() if the initial fopen() fails.
CODA_OSS_API FILE* fopen(const coda_oss::filesystem::path&, const std::string& mode);
CODA_OSS_API int open(const coda_oss::filesystem::path&, int flags);
CODA_OSS_API int open(const coda_oss::filesystem::path&, int flags, int mode);
CODA_OSS_API int close(int fd); // needed to close a FD from open()

#ifdef _WIN32
#define CODA_OSS_stat _stat
#else
#define CODA_OSS_stat stat
#endif
// Call  sys::expandEnvironmentVariables() if the initial stat() attempt fails.
CODA_OSS_API int stat(const coda_oss::filesystem::path&, struct CODA_OSS_stat &buffer);

// Call  sys::expandEnvironmentVariables() if the initial open attempt fails.
CODA_OSS_API std::ifstream make_ifstream(const coda_oss::filesystem::path&, std::ios_base::openmode mode = std::ios_base::in); // https://en.cppreference.com/w/cpp/io/basic_ifstream/basic_ifstream
CODA_OSS_API void open(std::ifstream&, const coda_oss::filesystem::path&, std::ios_base::openmode mode = std::ios_base::in); // https://en.cppreference.com/w/cpp/io/basic_ifstream/open

}

#endif  // CODA_OSS_sys_File_h_INCLUDED_
