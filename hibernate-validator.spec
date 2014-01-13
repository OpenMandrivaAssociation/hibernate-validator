%{?_javapackages_macros:%_javapackages_macros}
%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}
%global majorversion 5
Name:          hibernate-validator
Version:       5.0.1
Release:       1.0%{?dist}
Summary:       Bean Validation 1.1 (JSR 349) Reference Implementation
License:       ASL 2.0
URL:           http://www.hibernate.org/subprojects/validator.html
Source0:       https://github.com/hibernate/hibernate-validator/archive/%{namedversion}.tar.gz
# JAXB2 and JDK7 problems see https://hibernate.atlassian.net/browse/HV-528
Patch0:        %{name}-5.0.1.Final-jaxb.patch
BuildRequires: java-devel

BuildRequires: cdi-api
BuildRequires: bean-validation-api
BuildRequires: classmate
BuildRequires: glassfish-annotation-api
BuildRequires: glassfish-el
BuildRequires: glassfish-el-api
BuildRequires: glassfish-jaxb
BuildRequires: glassfish-jaxb-api
BuildRequires: hibernate-jpa-2.1-api
BuildRequires: jboss-interceptors-1.2-api
BuildRequires: jboss-logging >= 3.1.1
# 1.7.1
BuildRequires: jsoup
BuildRequires: joda-time
BuildRequires: junit

BuildRequires: jaxb2-maven-plugin
# 1.0.3.Final
BuildRequires: jboss-logging-tools
BuildRequires: maven-local
#BuildRequires: maven-dependency-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-injection-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-processor-plugin
%if 0
BuildRequires: beanvalidation-tck
BuildRequires: maven-failsafe-plugin
%endif

BuildArch:     noarch

%description
This is the reference implementation of JSR-349 - Bean Validation 1.1.
Bean Validation defines a meta-data model and API for JavaBean as well
as method validation. The default meta-data source are annotations,
with the ability to override and extend the meta-data through the
use of XML validation descriptors.

%package annotation-processor
Summary:       Hibernate Validator Annotation Processor

%description annotation-processor
Hibernate Validator Annotation Processor.

%package cdi
Summary:       Hibernate Validator Portable Extension

%description cdi
Hibernate Validator CDI Portable Extension.

%package performance
Summary:       Hibernate Validator Performance Tests

%description performance
Hibernate Validator performance tests.

%if 0
%package integration
Summary:       Hibernate Validator AS Integration Tests

%description integration
Hibernate Validator integration tests.

%package tck-runner
Summary:       Hibernate Validator TCK Runner

%description tck-runner
Aggregates dependencies and runs the JSR-349 TCK.
%endif

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
find . -name "*.jar" -delete
# tck-runner/src/as7config/modules/org/jboss/as/ee/main/jboss-as-ee-7.1.1.Final.jar
%pom_disable_module distribution
%pom_disable_module documentation
# documentation plugins
%pom_remove_plugin :maven-jdocbook-plugin
%pom_remove_plugin org.zanata:zanata-maven-plugin
# tck-runner and documentation plugins
%pom_remove_plugin org.codehaus.gmaven:gmaven-plugin
%pom_remove_plugin org.codehaus.gmaven:gmaven-plugin integration
%pom_remove_plugin org.codehaus.mojo:animal-sniffer-maven-plugin
%pom_remove_plugin org.codehaus.mojo:clirr-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-surefire-report-plugin
%pom_remove_plugin org.codehaus.mojo:chronos-jmeter-maven-plugin

%pom_remove_plugin org.apache.maven.plugins:maven-surefire-report-plugin engine
%pom_remove_plugin org.codehaus.mojo:chronos-jmeter-maven-plugin performance
%pom_remove_plugin org.codehaus.mojo:chronos-report-maven-plugin performance

%pom_xpath_remove "pom:build/pom:extensions"
# groovy 2.1.0
%pom_remove_dep org.codehaus.groovy:groovy-jsr223
# 2.0.0.CR2
%pom_remove_dep org.jboss.weld:weld-core
%pom_remove_dep org.jboss.as:jboss-as-arquillian-container-managed
%pom_remove_dep org.jboss.arquillian.container:arquillian-weld-se-embedded-1.1
%pom_remove_dep org.jboss.arquillian:arquillian-bom
%pom_remove_dep :fest-assert
%pom_remove_dep :easymock
%pom_remove_dep :log4j
%pom_remove_dep :slf4j-log4j12
%pom_remove_dep :testng

%pom_remove_plugin :maven-dependency-plugin tck-runner
%pom_remove_plugin :maven-surefire-report-plugin tck-runner
%pom_remove_plugin :maven-dependency-plugin annotation-processor

%pom_xpath_remove "pom:dependencies/pom:dependency[pom:scope ='test']" annotation-processor
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:scope ='test']" cdi
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:scope ='test']" engine
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:scope ='test']" integration
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:scope ='test']" tck-runner

%patch0 -p1

%pom_disable_module integration
%pom_disable_module tck-runner


%build
%mvn_package ":%{name}-parent" %{name}
# Running tests requires hibernate proper (and require weld-core >= 2.0.0 groovy >= 2.1.0), so skip for now:
%mvn_build -f -s -- -Pdist

%install
%mvn_install

install -m 644 engine/target/hibernate-validator-%{namedversion}-testing.jar \
    %{buildroot}%{_javadir}/%{name}/%{name}-testing.jar

%files -f .mfiles-%{name}
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}-testing.jar
%doc CONTRIBUTING.md README.md changelog.txt copyright.txt license.txt

%files annotation-processor -f .mfiles-%{name}-annotation-processor
%doc license.txt

%files cdi -f .mfiles-%{name}-cdi
%doc license.txt

%files performance -f .mfiles-%{name}-performance
%doc license.txt

%if 0
%files integration -f .mfiles-%{name}-integrationtest-as
%doc license.txt

%files tck-runner -f .mfiles-%{name}-tck-runner
%doc license.txt
%endif

%files javadoc -f .mfiles-javadoc
%doc license.txt

%changelog
* Thu May 09 2013 gil cattaneo <puntogil@libero.it> 5.0.1-1
- update to 5.0.1.Final
- adapted to current guideline
- switch to XMvn

* Fri Feb 22 2013 Juan Hernandez <juan.hernandez@redhat.com> - 4.2.0-8
- Remove the wagon-webdav build extension (rhbz 914076)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 4.2.0-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 5 2012 Juan Hernandez <juan.hernandez@redhat.com> - 4.2.0-4
- Cleanup of the spec file
- Replace jaxb2-maven-plugin with maven-jaxb2-plugin

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> - 4.2.0-3
- Building all classes with jaxb2 xjc target

* Wed Dec 14 2011 Andy Grimm <agrimm@gmail.com> - 4.2.0-2
- include both pom files, with correct names

* Tue Oct 18 2011 Andy Grimm <agrimm@gmail.com> - 4.2.0-1
- Initial package
