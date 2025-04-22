from core.disk import Disk

disk = Disk()
home = disk.create_partition('home/', 16384)
usr = disk.create_partition('usr/', 16384)
etc = disk.create_partition('etc/', 16384)
mnt = disk.create_partition('mnt/', 8192)

print(disk)
print(home)
print(usr)
print(etc)
print(mnt)
for block in disk.blocks:
    print(block)
