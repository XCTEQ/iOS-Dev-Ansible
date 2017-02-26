
[![CI Status](http://img.shields.io/travis/Shashikant86/iOS-Dev-Ansible.svg?style=flat)](https://travis-ci.org/Shashikant86/iOS-Dev-Ansible)

Ansible Provisioning of iOS Development & Continuous Integration
=========

This role can be used to setup iOS Continuous Integration Service on macOS. This role also can be used for the setting up local development environment for the iOS Developer. It has all the tools required for the iOS Developers like Xcode, Swift Fastlane, Carthage, Cocoapods and lot's of homebrew packages, however you can have full control to configure your own environment with variables.  Xcode installation needs pre-downloaded XIP file but installing simulators and command line tools has been automated by this role. This role is fully tested for

* macOS Seirra
* Xcode 8.0.2
* Xcode 8.3 beta xip

This should work from Xcode 8 onward as `xip` format is supported from Xcode 8 onwards.  

Requirements
------------

* Install Ansible using pip
Ansible is python library so we can install using pip

           $ easy_install pip
           $ pip install ansible

### Xcode Setup Requirements

There are couple of ways this role can install Xcode, you can pick one that is suitable for you  

* Xcode XIP/DMG in `files` directory of playbook

You should place a `dmg` or `xip` in the `files/` directory of your playbook
for this role to pick it up and transfer it over. You must turn set the variables `configure_xcode_playbook_files` to `yes` enable this mode. There are couple of variables, we can use to use this approach. We can use `xcode_major_version` to specify exact version of the Xcode we are using and `xcode_src` file name of Xcode DMG/XIP to copy over to other machines. The example will look like this:

```
configure_xcode_playbook_files: yes
xcode_major_version: 8.2
xcode_src: Xcode_8.2.xip
```


This allows us to install a specific version (good for CI stability) and avoids
the role dealing with authenticating with the Apple Developer Portal.

*  Download Xcode from Apple App Store using MAS CLI

This approach need your Apple Developer ID and Password to set into the config/variables file. This will download Xcode from the macOS Apple Store. which takes lot of time.
The variables we can set are as below, you can put your app_id and credentials there !!

```
use_mac_store: yes
mas_email: ""
mas_password: ""
mas_installed_apps:
  - { id: 497799835, name: "Xcode (8.1)" }

mas_upgrade_all_apps: no

```

You can choose one of the above approach to install Xcode but It's recommended to use first approach 'Xcode XIP/DMG in `files` directory of playbook'.  

What's in this role:
--------------
This role comes with following softwares packages to provision iOS Continuous Integration Server.

* Xcode Installation
* Swiftenv : Version manager for Swift
* iOS Dependency Management tools like Carthage, Cocoapods and Swift Package Manager.
* iOS Continuous Delivery tools i.e Fastlane tools
* macOS defaults : Controls defaults and Software Updates
* Homebrew : Package Manager for macOS
* Homebrew packages like git, carthage, swiftlint, mas, cmake, RVM, curl, wget etc etc
* Homebrew Cask packages
* RVM and customised Ruby versions
* Pre-installed Gems like bundler, Fastlane, Cocoapods, Xcpretty
* Xcode 8
* Install Command Line Tools for the Xcode
* Install Xcode Simulator (9.2 but you can change anytime)

You can customise your own playbook to override defaults and create your own playbook.

Role Variables:
----------------

This role has lot of variables which can be used to configure your own playbook. Please refer `defaults/main.yml` for list of all variables. **You can override `defaults/main.yml` variables to configure your own**. The main variables are :

### Xcode Related Variables

* `configure_xcode_documents_dir`
You can skip the Xcode Configuration by setting that to `no`, then it won't install Xcode, Xcode Command Line tools and simulators. You can enable Xcode installation by placing Xcode XIP in the `~/Documents/` directory and set the variable to `yes`.

* `configure_xcode_playbook_files`
You can put Xcode XIP/DMG inside `files` directory of the playbook and use below mentioned variables to install Xcode

```
configure_xcode_playbook_files: yes
xcode_major_version: 8.2
xcode_src: Xcode_8.2.xip

```

* Xcode using Mac App Store and MAS CLI
You can get Xcode from Mac App Store but it requires your Apple Developers Credentials so be careful !
Variables to set are

```
use_mac_store: yes
mas_email: ""
mas_password: ""
mas_installed_apps:
  - { id: 497799835, name: "Xcode (8.1)" }

mas_upgrade_all_apps: no

```


### Custom Swift and Ruby Version Manager Variables

* `configure_custom_swift`
Xcode 8 comes with default Swift however we can use different Swift toolchain. You can set it to `yes` then you need to configure `swift_version_custom` varibale with value of Swift version that you want e.g `3.0.1`

* `configure_ruby_rvm`
macOS comes with default Ruby `2.0.0` but it's hard to manage Rubygems using system Ruby. We can use version management tools like RVM by setting `configure_ruby_rvm` varibale to `yes` and setting `ruby-version` value to Ruby version we want e.g `2.4.0`

### macOS Defaults and Software Updates Related Varibales

You can turn **ON** or **OFF** the macOS defaults defaults by putting commands inside the variables `macos_sleep_options`, `macos_animation_options` and `macos_software_autoupdates` e.g

```
macos_sleep_options:
  - systemsetup -setsleep Never
  - systemsetup -setharddisksleep Never

```
### Homebrew Related Varibales

You can customise Homebrew installtion path using `homebrew_install_path` and list of packages using `homebrew_installed_packages` and Homebrew Cask Applications using ` homebrew_cask_apps` variables. You can also list the Homebrew taps using `homebrew_taps` Varibales.



How to use this Role:
--------------

Imagine, you have fresh Mac with fresh macOS installed. You can setup all your iOS Development environment by creating Playbook for this role. You can setup config variables as per your need.

Assuming you have installed Ansible, we can download the role by running command

           $ $ ansible-galaxy install Shashikant86.iOS-Dev

Now that, we have to create our own playbook for this role by setting variables,  We can use `defaults/main.tml` file [here](https://github.com/Shashikant86/iOS-Dev-Ansible/blob/master/defaults/main.yml). The example playbook looks like this


Example Playbook
----------------

We can created `playbook.yml` like this

```
---
- hosts: localhost
  connection: local
  remote_user: root

  vars:
    configure_xcode: no
    configure_custom_swift: yes
    configure_macos_defaults: no
    configure_ruby_rvm: yes
    homebrew_upgrade_all_packages: no
    use_mac_store: no


    xcode_src: Xcode_8.2.1.xip

    ruby_version: 2.4.0
    rubygems_packages_to_install:
      - bundler
      - xcpretty

    swift_version_custom: 3.0.1

    homebrew_installed_packages:
      - autoconf
      - bash-completion
      - git
      - carthage
      - gpg
      - boost
      - cmake
      - ssh-copy-id
      - openssl
      - wget
      - curl
      - argon/mas/mas
      - kylef/formulae/swiftenv

    homebrew_taps:
      - homebrew/core
      - caskroom/cask
      - homebrew/binary
      - homebrew/dupes
      - homebrew/versions


    homebrew_cask_apps:
      - java

  roles:
    - Shashikant86.iOS-Dev


```

Please refer playbook/config inside the `tests` directory as an example.

You can create `config.yml` an call this from playbook file if you want to keep variables out of playbook file


Setting up Continuous Intrgration with Travis
------------

We can test this role on TravisCI by disabling the Xcode config as TravisCI has it's own Xcode images. We can test all other things on TravisCI. You can see the TravisCI config in the `.travis.yml` and playbook/config inside the `tests` directory. You can see TravisCI output [here](https://travis-ci.org/Shashikant86/iOS-Dev-Ansible/builds/203170430)


Dependencies
------------

None



License
-------

MIT

Author Information
------------------

Shashikant Jagtap
