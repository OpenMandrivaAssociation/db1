%define name db1
%define version 1.85
%define url http://www.sleepycat.com/update
%define release 12mdk

Summary: The BSD database library for C (version 1).
Name: %{name}
Version: %{version}
Release: %{release}
Source: %{url}/%{version}/db.%{version}.tar.bz2
Patch: db.%{version}.patch
Patch1: db.%{version}-include.patch
URL: http://www.sleepycat.com
License: BSD
Group: System/Libraries
PreReq: /sbin/ldconfig
BuildRoot: %{_tmppath}/%{name}-root
Prefix: %{_prefix}
# this is a symlink not a real soname, so it has to be explicitely put
# in a provides line -- pablo
Provides: libdb1.so.2
%ifnarch ia64
Conflicts: glibc < 2.1.90
%endif

%package devel
Summary: Development libs/header files for Berkeley DB (version 1) library.
Group: Development/C
Prefix: %{_prefix}
Requires: %{name} = %{version}
%ifnarch ia64
Conflicts: glibc-devel < 2.1.90
%endif
%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
It should be installed if compatibility is needed with databases created
with db1.
This library used to be part of the glibc package.

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B tree, Hashing, Fixed and Variable-length
record access methods.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%package tools
Summary: Tools for Berkeley DB (version 1) library.
Group: Databases
Prefix: %{_prefix}

%description tools
Tools to manipulate Berkeley Databases (Berkeley DB).

%prep
%setup -q -n db.%{version}
%patch -p1
%patch1 -p1 -b .old

%build
gzip -9 docs/*.ps
cd PORT/linux
# otherwise "db1/db.h" not found
ln -s include db1
%make OORG="$RPM_OPT_FLAGS" 

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/db1
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}

sed -n '/^\/\*-/,/^ \*\//s/^.\*.\?//p' include/db.h | grep -v '^@.*db\.h' > LICENSE

cd PORT/linux
sover=`echo libdb.so.* | sed 's/libdb.so.//'`
install -m644 libdb.a			$RPM_BUILD_ROOT/%{_libdir}/libdb1.a
install -m755 libdb.so.$sover		$RPM_BUILD_ROOT/%{_libdir}/libdb1.so.$sover
ln -sf libdb1.so.$sover 		$RPM_BUILD_ROOT/%{_libdir}/libdb1.so
ln -sf libdb1.so.$sover			$RPM_BUILD_ROOT/%{_libdir}/libdb.so.$sover
install -m644 ../include/ndbm.h		$RPM_BUILD_ROOT/%{_includedir}/db1/
install -m644 ../../include/db.h	$RPM_BUILD_ROOT/%{_includedir}/db1/
install -m644 ../../include/mpool.h	$RPM_BUILD_ROOT/%{_includedir}/db1/
install -s -m755 db_dump185		$RPM_BUILD_ROOT/%{_bindir}/db1_dump185

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README LICENSE changelog
%{_libdir}/libdb1.so.*
%{_libdir}/libdb.so.*

%files devel
%defattr(-,root,root)
%doc docs/*.ps.gz
%{_includedir}/db1
%{_libdir}/libdb1.a
%{_libdir}/libdb1.so

%files tools
%defattr(-,root,root)
%{_bindir}/db1_dump185

