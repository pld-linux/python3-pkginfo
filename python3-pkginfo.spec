#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Query metadata from sdists/bdists/installed packages
Summary(pl.UTF-8):	Odpytywanie medatanych z sdist/bdist/pakietów zainstalowanych
Name:		python3-pkginfo
Version:	1.12.1.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pkginfo/
Source0:	https://files.pythonhosted.org/packages/source/p/pkginfo/pkginfo-%{version}.tar.gz
# Source0-md5:	021f56d78ec93965b21e98bc3a3ab370
URL:		https://pypi.org/project/pkginfo/
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides an API for querying the distutils metadata
written in the PKG-INFO file inside a source distriubtion (an "sdist")
or a binary distribution (e.g., created by running "bdist_egg"). It
can also query the EGG-INFO directory of an installed distribution,
and the *.egg-info stored in a "development checkout" (e.g, created by
running "setup.py develop").

%description -l pl.UTF-8
Ten pakiet dostarcza API do odpytywania metadanych distutils,
zapisanych w pliku PKG-INFO wewnątrz dystrybucji źródłowej ("sdist")
lub dystrybucji binarnej (tj. utworzonej przez uruchomienie
"bdist_egg"). Potrafi także odpytywać katalog EGG-INFO zainstalowanej
dystrybucji oraz *.egg-info zapisane w deweloperskim zrzucie
(utworzonym np. przez uruchomienie "setup.py develop").

%package apidocs
Summary:	API documentation for Python pkginfo module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pkginfo
Group:		Documentation

%description apidocs
API documentation for Python pkginfo module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pkginfo.

%prep
%setup -q -n pkginfo-%{version}

%build
%py3_build

%if %{with tests}
# test_installed_ctor_w_dist_info doesn't support metadata >2.3 from recent pythons
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest pkginfo -k 'not test_installed_ctor_w_dist_info'
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pkginfo{,-3}
ln -s pkginfo-3 $RPM_BUILD_ROOT%{_bindir}/pkginfo

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/pkginfo/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt TODO.txt
%attr(755,root,root) %{_bindir}/pkginfo-3
%{_bindir}/pkginfo
%{py3_sitescriptdir}/pkginfo
%{py3_sitescriptdir}/pkginfo-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build/html/{_static,*.html,*.js}
%endif
