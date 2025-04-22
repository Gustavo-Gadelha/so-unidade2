from core.disk import Disk

disk = Disk()
home = disk.create_partition(16384)
usr = disk.create_partition(16384)
etc = disk.create_partition(16384)
mnt = disk.create_partition(8192)

disk.delete_partition(1)

disk.print_debug()

