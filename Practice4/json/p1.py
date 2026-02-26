import json
with open("sample-data.json", encoding="utf-8") as f:
    data=json.load(f)
interfaces=data["imdata"]
needed_ids=["eth1/33", "eth1/34", "eth1/35"]
filtered=[item for item in interfaces if item["l1PhysIf"]["attributes"]["id"] in needed_ids]
print("Interface Status")
print("="*80)
print(f"{'DN':50} {'Description':20} {'Speed':6} {'MTU':6}")
print("-"*50 + " " + "-"*20 + "  " + "-"*6 + "  " + "-"*6)
for item in filtered:
    attrs=item["l1PhysIf"]["attributes"]
    dn=attrs["dn"]
    descr=attrs.get("descr", "")
    speed=attrs.get("speed", "")
    mtu=attrs.get("mtu", "")
    print(f"{dn:<50} {descr:<20} {speed:>6} {mtu:>6}")