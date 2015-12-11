Name:		libds3
Version:	1.2.0
Release:	1%{?dist}
Vendor:		Globus Support
Summary:	Spectra S3 C SDK

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		https://github.com/SpectraLogic/ds3_c_sdk
Source:		https://github.com/SpectraLogic/ds3_c_sdk/archive/v%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	pkgconfig
BuildRequires:	libxml2-devel >= 2.9
BuildRequires:	libcurl-devel >= 7.29
BuildRequires:	glib2-devel >= 2.34
BuildRequires:	automake >= 1.11
BuildRequires:	autoconf >= 2.60
BuildRequires:	libtool >= 2.2

%package devel
Summary:	Spectra S3 C SDK Development Libraries
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description
Spectra S3 C SDK

%description devel
Spectra S3 C SDK Development Libraries and Headers

%prep
%setup -q -n ds3_c_sdk-%{version}

%build
%if %{?fedora}%{!?fedora:0} >= 22 || %{?rhel}%{!?rhel:0} >= 7
# Remove files that should be replaced during bootstrap
rm -rf autom4te.cache

mkdir -p m4
autoreconf -if
%endif

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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Dec 11 2015 Globus Toolkit <support@globus.org> - 1.2.0-1
- Initial package
