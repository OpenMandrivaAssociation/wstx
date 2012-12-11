# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

%define section         free

Name:           wstx
Summary:        Woodstox Stax Implementation
Version:        3.2.1
Release:        %mkrel 1.0.3
Epoch:          0
URL:            http://woodstox.codehaus.org/
License:        Apache License
Group:          Development/Java
Source0:         http://woodstox.codehaus.org/3.2.1/wstx-src-3.2.1.tar.gz
Source1:         wstx-asl-3.2.1.pom
Source2:         wstx-lgpl-3.2.1.pom

Patch0:         wstx-3.2.1-build_xml.patch

BuildRequires:  java-rpmbuild >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-apache-bcel
BuildRequires:  ant-nodeps
BuildRequires:  junit
BuildRequires:  bea-stax-api >= 0:1.2.0
#BuildRequires:  emma
BuildRequires:  msv-msv
BuildRequires:  msv-xsdlib
Requires:       bea-stax-api >= 0:1.2.0
Requires:       msv-msv
Requires:       msv-xsdlib

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
%if ! %{gcj_support}
BuildArch:      noarch
%endif
%if %{gcj_support}
BuildRequires:      java-gcj-compat-devel
%endif


%description
Woodstox is a high-performance validating namespace-aware 
StAX-compliant (JSR-173) Open Source XML-processor written 
in Java.
XML processor means that it handles both input (== parsing) 
and output (== writing, serialization)), as well as 
supporting tasks such as validation.

%package j2me
Group:          Development/Java
Summary:        J2ME libraries for %{name}

%description j2me
%{summary}.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
%{summary}.

%package manual
Group:          Development/Java
Summary:        Documents for %{name}

%description manual
%{summary}.

%prep
%setup -q -c -n %{name}

for f in $(find . -name '*.?ar'); do
      #mv $f $f.no
      rm $f
done

%patch0 -b .sav

pushd lib
#ln -sf $(build-classpath emma) .
#ln -sf $(build-classpath emma_ant) .
ln -sf $(build-classpath bea-stax-api) stax-api-1.0.jar
pushd msv
ln -sf $(build-classpath msv-msv) msv.jar
ln -sf $(build-classpath msv-xsdlib) xsdlib.jar
ln -sf $(build-classpath relaxngDatatype) .
popd
popd

%build
export OPT_JAR_LIST="`%{__cat} %{_sysconfdir}/ant.d/nodeps` `%{__cat} %{_sysconfdir}/ant.d/apache-bcel`"
%{ant} jars jars.j2me javadoc #test staxtest

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 644 build/stax2.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}/stax2-%{version}.jar
install -m 644 build/%{name}-api-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-api-%{version}.jar
install -m 644 build/%{name}-asl-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-asl-%{version}.jar
install -m 644 build/%{name}-lgpl-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-lgpl-%{version}.jar
install -m 644 build/%{name}-j2me-min-both.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-j2me-min-both-%{version}.jar
install -m 644 build/%{name}-j2me-min-input.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-j2me-min-input-%{version}.jar
install -m 644 build/%{name}-j2me-min-output.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-j2me-min-output-%{version}.jar
# create unversioned symlinks
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)

%add_to_maven_depmap org.codehaus.woodstox stax2 %{version} JPP/wstx stax2
%add_to_maven_depmap org.codehaus.woodstox wstx-api %{version} JPP/wstx wstx-api
%add_to_maven_depmap org.codehaus.woodstox wstx-asl %{version} JPP/wstx wstx-asl
%add_to_maven_depmap org.codehaus.woodstox wstx-lgpl %{version} JPP/wstx wstx-lgpl
%add_to_maven_depmap org.codehaus.woodstox wstx-j2me-min-both %{version} JPP/wstx wstx-j2me-min-both
%add_to_maven_depmap org.codehaus.woodstox wstx-j2me-min-input %{version} JPP/wstx wstx-j2me-min-input
%add_to_maven_depmap org.codehaus.woodstox wstx-j2me-min-output %{version} JPP/wstx wstx-j2me-min-output

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.wstx-wstx-asl.pom
install -pm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.wstx-wstx-lgpl.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr release-notes/* \
    $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%post j2me
%update_maven_depmap

%postun j2me
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/stax2*.jar
%{_javadir}/%{name}/%{name}-api*.jar
%{_javadir}/%{name}/%{name}-asl*.jar
%{_javadir}/%{name}/%{name}-lgpl*.jar
%{_datadir}/maven2/poms/*
%config(noreplace) %{_mavendepmapfragdir}/wstx
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-*-%{version}.jar.*
%endif

%files j2me
%defattr(0644,root,root,0755)
%{_javadir}/%{name}/%{name}-j2me-min-both*.jar
%{_javadir}/%{name}/%{name}-j2me-min-input*.jar
%{_javadir}/%{name}/%{name}-j2me-min-output*.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}



%changelog
* Sun Sep 20 2009 Thierry Vignaud <tvignaud@mandriva.com> 0:3.2.1-1.0.3mdv2010.0
+ Revision: 445825
- rebuild

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 0:3.2.1-1.0.2mdv2009.1
+ Revision: 350078
- 2009.1 rebuild

* Fri Dec 28 2007 David Walluck <walluck@mandriva.org> 0:3.2.1-1.0.1mdv2008.1
+ Revision: 138992
- import wstx


* Mon May 28 2007 Ralph Apel <r.apel at r-apel.de> 0:3.2.1-1jpp
- Upgrade to 3.2.1
- Add gcj_support option
- Install poms, depmap frags

* Fri May 05 2006 Ralph Apel <r.apel@r-apel.de> 0:2.9.3-1jpp
- First build

