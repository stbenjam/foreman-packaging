%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%if 0%{?scl:1}
    %global root_bindir %{_root_bindir}
    %global root_sysconfdir %{_root_sysconfdir}
%else
    %global root_bindir %{_bindir}
    %global root_sysconfdir %{_sysconfdir}
%endif

%global gem_name smart_proxy_dynflow_core
%global service_name smart_proxy_dynflow_core

Summary: Core Smart Proxy Dynflow Service
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.1.3
Release: 1%{?foremandist}%{?dist}
Group: Development/Libraries
License: GPLv3
URL: http://github.com/theforeman/smart_proxy_dynflow
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: foreman-proxy >= 1.11.0

Requires: %{?scl_prefix}rubygem(bundler_ext)
Requires: %{?scl_prefix}rubygem(dynflow) >= 0.8.4
Requires: %{?scl_prefix}rubygem(dynflow) < 0.9.0
Requires: %{?scl_prefix}rubygem(sequel)
Requires: %{?scl_prefix}rubygem(rest-client)
Requires: %{?scl_prefix_ror}rubygem(sinatra) >= 1.4
Requires: %{?scl_prefix_ror}rubygem(sinatra) < 2.0
Requires: %{?scl_prefix_ror}rubygem(rack)
Requires: %{?scl_prefix_ror}rubygem(sqlite3)
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}rubygems
%if 0%{?rhel} == 6
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
%else
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
BuildRequires: systemd
%endif

BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems
BuildRequires: %{?scl_prefix_ruby}rubygems-devel

BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Use the Dynflow inside Foreman smart proxy

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} - <<EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build
sed -ri 'sX.*/usr/bin/ruby|/usr/bin/env ruby.*$X\#\!/usr/bin/%{?scl:%{scl_prefix}}rubyX' .%{_bindir}/%{service_name}

# switches to bundler_ext instead of bundler
mv ./%{gem_instdir}/Gemfile ./%{gem_instdir}/Gemfile.in
sed -ri 'sX\#\{File\.dirname\(__FILE__\)\}/bundler\.d/\*\.rbX%{_datadir}/%{gem_name}/bundler.d/*.rbX' ./%{gem_instdir}/Gemfile.in

%install
mkdir -p %{buildroot}%{_datadir}/%{gem_name}/bundler.d

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{root_bindir}
cp -pa .%{_bindir}/* %{buildroot}%{root_bindir}/

mkdir -p %{buildroot}%{root_sysconfdir}/smart_proxy_dynflow_core
cp -pa .%{gem_instdir}/config/settings.yml.example %{buildroot}%{root_sysconfdir}/smart_proxy_dynflow_core/settings.yml

#copy init scripts and sysconfigs
%if 0%{?rhel} == 6
install -Dp -m0755 %{buildroot}%{gem_instdir}/deploy/%{service_name}.init %{buildroot}%{_root_initddir}/%{service_name}
%else
install -Dp -m0644 %{buildroot}%{gem_instdir}/deploy/%{service_name}.service %{buildroot}%{_unitdir}/%{service_name}.service
%endif

%post
%if 0%{?rhel} == 6
  /sbin/chkconfig --add %{service_name}
  exit 0
%else
  %systemd_post %{service_name}.service
%endif

%preun
%if 0%{?rhel} == 6
  if [ $1 -eq 0 ] ; then
    /sbin/service %{service_name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{service_name}
  fi
%else
  %systemd_preun %{service_name}.service
%endif

%postun
%if 0%{?rhel} != 6
  %systemd_postun_with_restart %{service_name}.service
%endif

%files
%dir %{gem_instdir}
%dir %{_datadir}/%{gem_name}/bundler.d
%exclude %{gem_instdir}/.*
%{gem_libdir}
%{gem_instdir}/bin
%{gem_instdir}/config
%{gem_instdir}/Gemfile.in
%{gem_instdir}/smart_proxy_dynflow_core.gemspec
%exclude %{gem_cache}
%{gem_spec}
%{root_sysconfdir}/%{gem_name}/settings.yml
%doc %{gem_instdir}/LICENSE
%{root_bindir}/%{service_name}
%if 0%{?rhel} == 6
%{_root_initddir}/%{service_name}
%else
%{_unitdir}/%{service_name}.service
%endif

%exclude %{gem_instdir}/deploy

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/LICENSE

%changelog
* Thu May 26 2016 Stephen Benjamin <stephen@redhat.com> 0.1.3-1
- Initial packaging of smart_proxy_dynflow_core
