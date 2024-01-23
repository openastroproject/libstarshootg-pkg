%define debug_package %{nil}

Name:           libstarshootg
Version:        1.55.24239
Release:        0
Summary:        Orion Starshoot G camera support library
License:	GPLv2+
Prefix:         %{_prefix}
Provides:       libstarshootg = %{version}-%{release}
Obsoletes:      libstarshootg < 1.55.24239
Source:         libstarshootg-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libstarshootg is a user-space driver for Orion Starshoot g astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libstarshootg-devel = %{version}-%{release}
Obsoletes:      libstarshootg-devel < 1.55.24239

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libstarshootg.pc.in > libstarshootg.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}/etc/udev/rules.d
mkdir -p %{buildroot}%{_includedir}

case %{_arch} in
  x86_64)
    cp x64/libstarshootg.bin %{buildroot}%{_libdir}/libstarshootg.so.%{version}
		cp starshootg.h %{buildroot}%{_includedir}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp 70-orion-cameras.rules %{buildroot}/etc/udev/rules.d

%post
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%files
%{_libdir}/*.so.*
%{_sysconfdir}/udev/rules.d/*.rules

%files devel
%{_includedir}/starshootg.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Jan 6 2024 James Fidell <james@openastroproject.org> - 1.55.24239-0
- Initial RPM release

