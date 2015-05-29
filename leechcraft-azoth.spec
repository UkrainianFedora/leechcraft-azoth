%define product_name leechcraft
%define plugin_dir %{_libdir}/%{product_name}/plugins-qt5
%define translations_dir %{_datadir}/%{product_name}/translations
%define settings_dir %{_datadir}/%{product_name}/settings
%define full_version %{version}-%{release}
%define git_version 3466-g864bd1a
%global optflags %(echo %{optflags} | sed 's/-D_FORTIFY_SOURCE=2 //')

Name:           leechcraft-azoth
Summary:        IM Client for LeechCraft
Version:        0.6.75
Release:        3%{?dist}
License:        GPLv2+
Url:            http://leechcraft.org
Source0:        http://dist.leechcraft.org/LeechCraft/%{version}/leechcraft-0.6.70-%{git_version}.tar.xz
Patch1:         001-fix-qwt-cmake-script.patch
Patch3:         003-fix-azoth-dependencies.patch

BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtwebkit-devel
BuildRequires: qwt-qt5-devel
BuildRequires: bzip2-devel
BuildRequires: pcre-devel
BuildRequires: qca2-devel
BuildRequires: qjson-devel
BuildRequires: qxmpp-devel
BuildRequires: speex-devel
BuildRequires: libotr-devel
BuildRequires: libpurple-devel
BuildRequires: openssl-devel
BuildRequires: libmsn-devel
BuildRequires: leechcraft-devel >= %{version}


%description
This package contains an IM client for LeechCraft.


%package devel
Summary:    Leechcraft Azoth Development Files
Requires:   %{name}%{?_isa} = %{full_version}

%description devel
This package contains header files required to develop new modules for
LeechCraft Azoth.


%prep
%setup -qn %{product_name}-0.6.70-%{git_version}
%patch1 -p 0
%patch3 -p 0


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLEECHCRAFT_VERSION="%{version}" \
    -DUSE_QT5=True \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    $(cat ../src/CMakeLists.txt | egrep "^(cmake_dependent_)?option \(ENABLE" | awk '{print $2}' | sed 's/^(/-D/;s/$/=False/;s/\(AZOTH[^=]*=\)False/\1True/' | xargs) \
    $(cat ../src/plugins/azoth/CMakeLists.txt | egrep "^option \(ENABLE" | awk '{print $2}' | sed 's/^(/-D/;s/$/=True/;s/\(WOODPECKER\|ASTRALITY\|SARIN\)=True/\1=False/' | xargs) \
    ../src

cd plugins/azoth
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd %{_target_platform}/plugins/azoth
make install/fast DESTDIR=$RPM_BUILD_ROOT
popd

declare -a arr=("leechcraft_azoth"\
                "leechcraft_azoth_acetamide"\
                "leechcraft_azoth_adiumstyles"\
                "leechcraft_azoth_autoidler"\
                "leechcraft_azoth_autopaste"\
                "leechcraft_azoth_birthdaynotifier"\
                "leechcraft_azoth_chathistory"\
                "leechcraft_azoth_depester"\
                "leechcraft_azoth_herbicide"\
                "leechcraft_azoth_hili"\
                "leechcraft_azoth_isterique"\
                "leechcraft_azoth_juick"\
                "leechcraft_azoth_lastseen"\
                "leechcraft_azoth_metacontacts"\
                "leechcraft_azoth_modnok"\
                "leechcraft_azoth_mucommands"\
                "leechcraft_azoth_murm"\
                "leechcraft_azoth_nativeemoticons"\
                "leechcraft_azoth_otroid"\
                "leechcraft_azoth_rosenthal"\
                "leechcraft_azoth_vader"\
                "leechcraft_azoth_xoox"\
                "leechcraft_azoth_xtazy"\
                "leechcraft_azoth_zheet"\ 
                "leechcraft_azoth_shx"\
                "leechcraft_azoth_standardstyles"\
                "leechcraft_azoth_abbrev"\
                "leechcraft_azoth_tracolor"\
                )

for i in "${arr[@]}"
do
   %find_lang $i --with-qt --without-mo
done

cat *.lang > azoth.lang


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f azoth.lang
%{plugin_dir}/libleechcraft_azoth*.so
%{_datadir}/applications/leechcraft-azoth-acetamide-qt5.desktop
%{_datadir}/applications/leechcraft-azoth-xoox-qt5.desktop
%{_datadir}/%{product_name}/azoth/emoticons/*
%{_datadir}/%{product_name}/azoth/iconsets/*
%{_datadir}/%{product_name}/azoth/styles/*
%{_datadir}/%{product_name}/azoth/lc_azoth_modnok_latexconvert.sh
%{settings_dir}/*.xml


%files devel
%{_includedir}/%{product_name}/*

%changelog
* Fri May 29 2015 Minh Ngo <minh@fedoraproject.org> - 0.6.75-1
- Qt5, 0.6.75

* Sat Dec 27 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.70-2
- Fixing bogus date

* Fri Dec 26 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.70-1
- 0.6.70

