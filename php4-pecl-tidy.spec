%define		_modname	tidy
%define		_status		stable
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - Tidy HTML Repairing and Parsing
Summary(pl):	%{_modname} - Czyszczenie, naprawa oraz parsowanie HTML
Name:		php4-pecl-%{_modname}
Version:	1.1
Release:	2
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	ecb2d3c62e1d720265a65dfb7e00e081
URL:		http://pecl.php.net/package/tidy/
BuildRequires:	php4-devel
BuildRequires:	rpmbuild(macros) >= 1.248
BuildRequires:	tidy-devel
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tidy is a binding for the Tidy HTML clean and repair utility which
allows you to not only clean and otherwise manipluate HTML documents,
but also traverse the document tree using the Zend Engine 2 OO
semantics.

In PECL status of this package is: %{_status}.

%description -l pl
Tidy jest dowi±zaniem do narzêdzia "Tidy HTML clean and repair", które
pozwala nie tylko na czyszczenie oraz manipulacjê dokumentami HTML,
ale tak¿e na przemierzanie przez strukturê dokumentu za pomoc±
zorientowanej obiektowo semantyki silnika Zend Engine 2.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d

%{__make} -C %{_modname}-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,TODO,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
