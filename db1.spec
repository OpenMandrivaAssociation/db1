%define libname %mklibname db 1

Summary:	The BSD database library for C (version 1)
Name:		db1
Version:	1.85
Release:	31
License:	BSD
Group:		System/Libraries
Url:		ftp://ftp.sleepycat.com/releases
Source0:	%{url}/db.%{version}.tar.bz2
Source100:	db1.rpmlintrc
Patch0:		db.%{version}.patch
Patch1:		db.%{version}-include.patch
Patch2:		db.1.85-LDFLAGS.diff
BuildRequires:	bzip2

%package -n %{libname}
Summary:	The BSD database library for C (version 1)
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%package -n %{libname}-devel
Summary:	Development libs/header files for Berkeley DB (version 1) library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
It should be installed if compatibility is needed with databases created
with db1.

%description -n %{libname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
It should be installed if compatibility is needed with databases created
with db1.

%description -n %{libname}-devel
This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%package tools
Summary:	Tools for Berkeley DB (version 1) library
Group:		Databases
Prefix:		%{_prefix}

%description tools
Tools to manipulate Berkeley database (version 1) databases.

%prep
%setup -qn db.%{version}
%apply_patches

%build
bzip2 docs/*.ps
cd PORT/linux
# otherwise "db1/db.h" not found
ln -s include db1
%make CC=%{__cc} OORG="%{optflags}" LDFLAGS="%{ldflags}"

%install
mkdir -p %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_bindir}

sed -n '/^\/\*-/,/^ \*\//s/^.\*.\?//p' include/db.h | grep -v '^@.*db\.h' > LICENSE

cd PORT/linux
sover=`echo libdb.so.* | sed 's/libdb.so.//'`
install -m644 libdb.a %{buildroot}/%{_libdir}/libdb1.a
install -m755 libdb.so.$sover %{buildroot}/%{_libdir}/libdb1.so.$sover
ln -sf libdb1.so.$sover %{buildroot}/%{_libdir}/libdb1.so
ln -sf libdb1.so.$sover %{buildroot}/%{_libdir}/libdb.so.$sover
install -m644 ../include/ndbm.h %{buildroot}/%{_includedir}/db1/
install -m644 ../../include/db.h %{buildroot}/%{_includedir}/db1/
install -m644 ../../include/mpool.h %{buildroot}/%{_includedir}/db1/
install -m755 db_dump185 %{buildroot}/%{_bindir}/db1_dump185

%files -n %libname
%{_libdir}/libdb1.so.*
%{_libdir}/libdb.so.*

%files -n %libname-devel
%doc docs/*.ps.bz2 README changelog
%{_includedir}/db1
%{_libdir}/libdb1.a
%{_libdir}/libdb1.so

%files tools
%{_bindir}/db1_dump185

