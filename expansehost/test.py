from expansehost.server import KVMServer

kvm = KVMServer(287, "d995507c-60dd-41cf-acde-2eaab51eb9af")
kvm_data = kvm.getServerData()

print(kvm_data)