#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-pkginfo.spec)

Summary:	Query metadata from sdists/bdists/installed packages
Summary(pl.UTF-8):	Odpytywanie medatanych z sdist/bdist/pakietów zainstalowanych
Name:		python-pkginfo
# keep 1.8.x here for python2 support
Version:	1.8.3
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pkginfo/
Source0:	https://files.pythonhosted.org/packages/source/p/pkginfo/pkginfo-%{version}.tar.gz
# Source0-md5:	e67d8f6e37ca37b5512384655bbce760
URL:		https://pypi.org/project/pkginfo/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-nose
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pynose
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
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

%package -n python3-pkginfo
Summary:	Query metadata from sdists/bdists/installed packages
Summary(pl.UTF-8):	Odpytywanie medatanych z sdist/bdist/pakietów zainstalowanych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-pkginfo
This package provides an API for querying the distutils metadata
written in the PKG-INFO file inside a source distriubtion (an "sdist")
or a binary distribution (e.g., created by running "bdist_egg"). It
can also query the EGG-INFO directory of an installed distribution,
and the *.egg-info stored in a "development checkout" (e.g, created by
running "setup.py develop").

%description -n python3-pkginfo -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
nosetests-%{py_ver} pkginfo
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# test_ctor_w_dist_info fails with metadata versions > 2.1 from newer pythons
PYTHONPATH=$(pwd) \
nosetests-%{py3_ver} pkginfo -e test_ctor_w_dist_info
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pkginfo{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pkginfo{,-3}
ln -s pkginfo-3 $RPM_BUILD_ROOT%{_bindir}/pkginfo
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt TODO.txt
%attr(755,root,root) %{_bindir}/pkginfo-2
%{py_sitescriptdir}/pkginfo
%{py_sitescriptdir}/pkginfo-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pkginfo
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt TODO.txt
%attr(755,root,root) %{_bindir}/pkginfo-3
%{_bindir}/pkginfo
%{py3_sitescriptdir}/pkginfo
%{py3_sitescriptdir}/pkginfo-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build/html/{_static,*.html,*.js}
%endif
