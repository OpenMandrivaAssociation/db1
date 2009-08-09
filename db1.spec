%define libname %mklibname db 1
%define name db1
%define version 1.85
%define release %mkrel 19

Summary: The BSD database library for C (version 1)
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{url}/db.%{version}.tar.bz2
Patch0: db.%{version}.patch
Patch1: db.%{version}-include.patch
Patch2: db.1.85-LDFLAGS.diff
URL: ftp://ftp.sleepycat.com/releases
License: BSD
Group: System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bzip2

%package -n %libname
Summary: The BSD database library for C (version 1)
Group: System/Libraries
Provides: db1
Obsoletes: db1

%package -n %libname-devel
Summary: Development libs/header files for Berkeley DB (version 1) library
Group: Development/C
Requires: %{libname} = %{version}
Provides: db1-devel
Obsoletes: db1-devel

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
It should be installed if compatibility is needed with databases created
with db1.

%description -n %libname
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
It should be installed if compatibility is needed with databases created
with db1.

%description -n %libname-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B tree, Hashing, Fixed and Variable-length
record access methods.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%package tools
Summary: Tools for Berkeley DB (version 1) library
Group: Databases
Prefix: %{_prefix}

%description tools
Tools to manipulate Berkeley database (version 1) databases.

%prep

%setup -q -n db.%{version}
%patch0 -p1
%patch1 -p1 -b .old
%patch2 -p0 -b .LDFLAGS

%build
bzip2 docs/*.ps
cd PORT/linux
# otherwise "db1/db.h" not found
ln -s include db1
%make OORG="$RPM_OPT_FLAGS" LDFLAGS="%{ldflags}"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{name}
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

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libdb1.so.*
%{_libdir}/libdb.so.*

%files -n %libname-devel
%defattr(-,root,root)
%doc docs/*.ps.bz2 README changelog
%{_includedir}/db1
%{_libdir}/libdb1.a
%{_libdir}/libdb1.so

%files tools
%defattr(-,root,root)
%{_bindir}/db1_dump185

