Name:		libds3
%global _commit 32ab3a88fffc21311670b6043ed8d8a882d019f6
%if %{?suse_version}%{!?suse_version:0} >= 1315
%global apache_license Apache-2.0
%else
%global apache_license ASL 2.0
%endif
%global soname 0
Version:	1.2.0g5
Release:	2%{?dist}
Vendor:		Globus Support
Summary:	Spectra S3 C SDK

Group:		System Environment/Libraries
License:        %{apache_license}
URL:		https://github.com/SpectraLogic/ds3_c_sdk
#Source:	https://github.com/SpectraLogic/ds3_c_sdk/archive/%{_commit}.tar.gz
Source:		https://downloads.globus.org/toolkit/gt6/packages/libds3-1.2.0g5.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	pkgconfig
BuildRequires:	libxml2-devel >= 2.9
BuildRequires:	libcurl-devel >= 7.29
BuildRequires:	glib2-devel >= 2.34
BuildRequires:	automake >= 1.11
BuildRequires:	autoconf >= 2.60
BuildRequires:	libtool >= 2.2

%if %{?suse_version}%{!?suse_version:0} >= 1315
%global mainpkg %{name}-%{soname}
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0} != 0
%package %{nmainpkg}
Summary:	Spectra S3 C SDK
Group:          System Environment/Libraries
%description %{nmainpkg}
Spectra S3 C SDK Development Libraries and Headers
%endif

%package devel
Summary:	Spectra S3 C SDK Development Libraries
Group:		Development/Libraries
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}

%description
Spectra S3 C SDK

%description devel
Spectra S3 C SDK Development Libraries and Headers

%prep
%setup -q -n ds3_c_sdk-%{_commit}

%build
# Remove files that should be replaced during bootstrap
rm -rf autom4te.cache

mkdir -p m4
autoreconf -if

%configure \
           --disable-static \
           --docdir=%{_docdir}/%{name}-%{version} \
           --includedir=%{_includedir}/%{name}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool archives (.la files)
find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;

%check
make %{?_smp_mflags} check

%clean
rm -rf $RPM_BUILD_ROOT

%post %{?nmainpkg} -p /sbin/ldconfig

%postun %{?nmainpkg} -p /sbin/ldconfig

%files %{?nmainpkg}  
%defattr(-,root,root,-)
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Mar 20 2018 Globus Toolkit <support@globus.org> - 1.2.0g5-2
- packaging fixes

* Fri Jan 27 2017 Globus Toolkit <support@globus.org> - 1.2.0-9
- fix SLES package

* Fri Dec 11 2015 Globus Toolkit <support@globus.org> - 1.2.0-8
- Update to latest upstream

* Fri Dec 11 2015 Globus Toolkit <support@globus.org> - 1.2.0-1
- Initial package
