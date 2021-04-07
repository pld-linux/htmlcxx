#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	A simple non-validating CSS1 and HTML parser for C++
Name:		htmlcxx
Version:	0.87
Release:	1
License:	LGPLv2 and GPLv2+ and ASL 2.0 and MIT
Group:		Development/Libraries
Source0:	http://downloads.sourceforge.net/htmlcxx/%{name}-%{version}.tar.gz
# Source0-md5:	3f6429102fc0670c31ac589e8cd7543c
URL:		http://htmlcxx.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	skip_post_check_so libcss_parser_pp.so.*

%description
htmlcxx is a simple non-validating html parser library for C++. It
allows to fully dump the original html document, character by
character, from the parse tree. It also has an intuitive tree
traversal API.

%package devel
Summary:	Headers and Static Library for htmlcxx
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The htmlcxx-devel package contains libraries and header files for
developing applications that use htmlcxx.

%description devel -l pl.UTF-8
Pakiet htmlcxx-devel zawiera pliki nagłówkowe i dokumentację potrzebne
do kompilowania aplikacji korzystających z htmlcxx.

%package static
Summary:	htmlcxx static library
Summary(pl.UTF-8):	Statyczna biblioteka htmlcxx
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The htmlcxx-static package contains the static libraries of htmlcxx.

%description static -l pl.UTF-8
Statyczna wersja biblioteki htmlcxx.

%prep
%setup -q

# convert to utf8 due rpmlint warning W: file-not-utf8 %{_docdir}/htmlcxx/AUTHORS
# convert to utf8 due rpmlint warning W: file-not-utf8 %{_docdir}/htmlcxx/README
iconv -f iso8859-1 -t utf-8 AUTHORS > AUTHORS.conv && mv -f AUTHORS.conv AUTHORS
iconv -f iso8859-1 -t utf-8 README > README.conv && mv -f README.conv README

%build
autoupdate
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static} \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# remove all '*.la' files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README COPYING LGPL_V2 ASF-2.0
%attr(755,root,root) %{_bindir}/htmlcxx
%attr(755,root,root) %{_libdir}/libcss_parser.so.*.*.*
%attr(755,root,root) %{_libdir}/libcss_parser_pp.so.*.*.*
%attr(755,root,root) %{_libdir}/libhtmlcxx.so.*.*.*
%ghost %{_libdir}/libcss_parser.so.0
%ghost %{_libdir}/libcss_parser_pp.so.0
%ghost %{_libdir}/libhtmlcxx.so.3
%{_datadir}/htmlcxx

%files devel
%defattr(644,root,root,755)
%{_includedir}/htmlcxx
%{_libdir}/libcss_parser.so
%{_libdir}/libcss_parser_pp.so
%{_libdir}/libhtmlcxx.so
%{_pkgconfigdir}/htmlcxx.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcss_parser.a
%{_libdir}/libcss_parser_pp.a
%{_libdir}/libhtmlcxx.a
%endif
