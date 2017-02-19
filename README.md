
[![CI Status](http://img.shields.io/travis/Shashikant86/ansible-ios-ci.svg?style=flat)](https://travis-ci.org/Shashikant86/ansible-ios-ci)

Ansible Provisioning of iOS Development & Continuous Integration
=========

This role can be used to setup iOS Continuous Integration Service on macOS. This role also canbe used for the setting up local development environment for the iOS Developer. It has all the tools required for the iOS Developers like Xcode, Swift fastlane, carthage, cocoapods and lot's of homebrew packages, however you can have full control to configure your own environment with varibales.  Xcode installation needs pre-downloaded XIP file but installing simulators and command line tools has been automated by this role. This role is fully tested for

* macOS Seirra
* Xcode 8.0.2
* Xcode 8.3 beta xip

This should work from Xcode 8 onward as `xip` format is supported from Xcode 8 onwards.  

Requirements
------------

* Install Ansible using pip
Ansible is python library so we can install using pipefail

           $ easy_install pip
           $ pip install ansible

If you want to setup Xcode and related tools then

* Download Xcode XIP and Place it inside `~/Documents`
Downloading Xcode needs Apple Developer account and it's hard to automate Xcode Installation process. You need to have Xcode XIP file downloaded from Apple developer portal. **You must put it inside `~/Documents/` directory.**

It's not ideal but Xcode is proprietary software so only requirement is to put `xcode.xip` it inside `~/Documents/` directory.


What's in this role:
--------------
This role comes with following softwares packages to provision iOS Continuous Integration Server.

* Xcode
* Swiftenv : Version manager for Swift
* iOS Dependency Management tools like Carthage, Cocoapods and Swift Package Manager.
* iOS Continuous Delivery tools i.e Fastlane tools
* macOS defaults : Controls defaults and Software Updates
* Homebrew : Package Manager for macOS
* Homebrew packages like git, carthage, swiftlint, mas, cmake, rbenv, curl, wget etc etc
* Homebrew Cask packages
* RVM and customised Ruby versions
* Pre-installed Gems like bundler, fastlane, Cocoapods, xcpretty
* Xcode 8 + Installation Script when xip is in the `~/Documents/` directory
* Install Comand Line Tools for the Xcode
* Install Xcode Simulator (9.2 but you can change anytime)

You can customise your own playbook to overirde defaults and create your own playbook.

Role Varibales:
----------------

This role has lot of varibales which can be used to configure your own playbook. Please refer `defaults/main.yml` for list of all varibales. ** You can override `defaults/main.yml` varibales to configure your own **. The main varibales are :

### Xcode Related Variables

* `configure_xcode`
You can skip the Xcode Configuration by setting that to `no`, then it won't install Xcode, Xcode Command Line tools and simulators. You can enable Xcode installation by placing Xcode XIP in the `~/Documents/` directory and set the varibale to `yes`.

### Custom Swift and Ruby Version Manager Variables

* `configure_custom_swift`
Xcode 8 comes with default Swift however we can use different Swift toolchain. You can set it to `yes` then you need to configure `swift_version_custom` varibale with value of Swift version that you want e.g `3.0.1`

* `configure_ruby_rvm`
macOS comes with default Ruby `2.0.0` but it's hard to manage Rubygems using system Ruby. We can use version management tools like RVM by setting `configure_ruby_rvm` varibale to `yes` and setting `ruby-version` value to Ruby version we want e.g `2.4.0`

### macOS Defaults and Software Updates Related Varibales

You can turn **ON** or **OFF** the macOS defaults defaults by putting commands inside the varibales `macos_sleep_options`, `macos_animation_options` and `macos_software_autoupdates` e.g

```
macos_sleep_options:
  - systemsetup -setsleep Never
  - systemsetup -setharddisksleep Never
```
### Homebrew Related Varibales

You can customise Homebrew installtion path using `homebrew_install_path` and list of packages using `homebrew_installed_packages` and Homebrew Cask Applications using ` homebrew_cask_apps` varibales. You can also list the Homebrew taps using `homebrew_taps` Varibales.



How to use this Role:
--------------

Imagine, you have fresh Mac with fresh macOS installed. You can setup all your iOS Development environment by creating Playbook for this role. You can setup config varibales as per your need.

Assuming you have installed Ansible, we can download the role by running command

           $ $ ansible-galaxy install Shashikant86.iOS-Dev

Now that, we have to create our own playbook for this role by setting values in the `config.yml` files. We can use `defaults/main.tml` file [here](https://github.com/Shashikant86/ansible-ios-ci/blob/master/defaults/main.yml) then we can create a playbook to use this file as configuration. The example playbook looks like this





Example Playbook
----------------

Assuming that we have `config.yml` file at the same location as `playbook.yml` file. We can created `playbook.yml` like this

```
---
- hosts: all
  connection: local
  remote_user: root

  vars_files:
    - config.yml

  pre_tasks:
    - include_vars: "{{ item }}"
      with_fileglob:
        - ../config.yml

  roles:
    - Shashikant86.iOS-Dev

```

Please refer playbook/config inside the `tests` directory as an example.

You don't need to create `config.yml` file if you can use all the varibale inside the `playbook.yml`. This might cause playbook file became too lenthy.


Setting up Continuous Intrgration with Travis
------------

We can test this role on TravisCI by disabling the Xcode config as TravisCI has it's own Xcode images. We can test all other things on TravisCI. You can see the TravisCI config in the `.travis.yml` and playbook/config inside the `tests` directory. You can see TravisCI output [here](https://travis-ci.org/Shashikant86/ansible-ios-ci/builds/203048714)


Dependencies
------------

None



License
-------

MIT

Author Information
------------------

Shashikant Jagtap
