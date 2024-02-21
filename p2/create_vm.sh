#!/bin/bash

name="test"
path="/var/lib/libvirt/images/"
vm_img="jammy-server-cloudimg-amd64.img"
size="10G"
ram=1024
vcpus=1
os_variant="ubuntu22.04"
file_output_path="./"
network="default"

meta=$(cat <<-END
#cloud-config
instance_id: $name
local-hostname: $name
END
)

user=$(cat <<-END
#cloud-config
disable_root: false
users:
- name: root
  lock_passwd: false
  plain_text_passwd: 'root'
- name: ubuntu
  lock_passwd: false
  plain_text_passwd: 'ubuntu'
END
)

if [[ $(virsh list | grep $name) != "" ]]; then
    echo "VM already exists. Delete it to recreate it"
    exit
fi

if  [ ! -d $path$name ]; then
    mkdir $path$name
fi

currdir=$(pwd)
cd $path$name

# creating log file for any undirected output
touch logs
date >> logs

# create meta-data file
touch meta-data
echo "$meta" > meta-data
echo "Created meta-data file"

# create user-data file
touch user-data
echo "$user" > user-data
echo "Created user-data file"

# creating disk image
sudo qemu-img create -f qcow2 -F qcow2 -o backing_file=$path$vm_img $file_output_path$name.qcow2 >> logs
qemu-img resize $name.qcow2 $size >> logs
echo "Created disk image"

#creating iso files for cloud init
sudo genisoimage -output $file_output_path$name-cidata.iso -volid cidata -joliet -rock meta-data user-data >> logs
echo "Created ISO files for cloud init"

#creating the VM
sudo virt-install --virt-type kvm --name $name --ram $ram --vcpus=$vcpus --os-variant $os_variant --disk path=$file_output_path$name.qcow2,format=qcow2 --disk path=$file_output_path$name-cidata.iso,device=cdrom --import --network network=$network --noautoconsole >> logs
echo "Created VM"

cd $currdir
