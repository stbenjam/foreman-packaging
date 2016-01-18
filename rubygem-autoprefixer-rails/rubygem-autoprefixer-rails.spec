%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name autoprefixer-rails

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 5.2.1.3
Release: 1%{?dist}
Summary: Add vendor prefixes to CSS rules using values from caniuse.com
Group: Development/Languages
License: MIT
URL: https://github.com/ai/autoprefixer-rails
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix_ruby}rubygem(json)
Requires: %{?scl_prefix_ror}rubygem(execjs)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Parse CSS and add vendor prefixes to CSS rules using values from the Can I Use
website.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%{?scl:scl enable %scl - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
%setup -q -D -T -n  %{gem_name}-%{version}
%{?scl:scl enable %scl - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %scl - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%{gem_instdir}/vendor
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.rails3
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/autoprefixer-rails.gemspec
%{gem_instdir}/spec

%changelog
* Tue Jan 05 2016 Daniel Lobato <elobatocs@gmail.com> 5.2.1.3-1
- Initial package