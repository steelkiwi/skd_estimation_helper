# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_check_update = false
  config.vm.network "forwarded_port", guest: 8000, host: 8001
  config.vm.network "forwarded_port", guest: 5555, host: 5555
  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"
  config.vm.synced_folder ".", "/vagrant", type: :virtualbox
  config.vm.provider "virtualbox" do |vb|
  
    # Customize the amount of memory on the VM:
    vb.memory = "512"
    vb.cpus = "1"
  end
end
