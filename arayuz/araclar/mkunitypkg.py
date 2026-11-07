import os,sys,uuid,tarfile,io,zipfile
base=sys.argv[1]; out_pkg=sys.argv[2]; out_zip=sys.argv[3]
root=os.path.join(base,'Assets')
entries=[]
for dp,dns,fns in os.walk(root):
    dns.sort()
    for d in dns: entries.append((os.path.join(dp,d),True))
    for f in sorted(fns):
        if not f.endswith('.meta'): entries.append((os.path.join(dp,f),False))
# write .meta files next to assets (stable guid per path)
for p,isdir in entries:
    rel=os.path.relpath(p,base).replace(os.sep,'/')
    g=uuid.uuid5(uuid.NAMESPACE_URL,'olympos/'+rel).hex
    meta='fileFormatVersion: 2\nguid: %s\n'%g + ('folderAsset: yes\nDefaultImporter:\n  externalObjects: {}\n  userData: \n  assetBundleName: \n  assetBundleVariant: \n' if isdir else '')
    open(p+'.meta','w').write(meta)
with tarfile.open(out_pkg,'w:gz') as t:
    def add(name,data):
        ti=tarfile.TarInfo(name);ti.size=len(data);ti.mode=0o644;t.addfile(ti,io.BytesIO(data))
    for p,isdir in entries:
        rel=os.path.relpath(p,base).replace(os.sep,'/')
        g=uuid.uuid5(uuid.NAMESPACE_URL,'olympos/'+rel).hex
        add(g+'/pathname',rel.encode())
        add(g+'/asset.meta',open(p+'.meta','rb').read())
        if not isdir: add(g+'/asset',open(p,'rb').read())
with zipfile.ZipFile(out_zip,'w',zipfile.ZIP_DEFLATED) as z:
    for dp,dns,fns in os.walk(root):
        for f in fns:
            fp=os.path.join(dp,f);z.write(fp,os.path.relpath(fp,base))
print(len(entries),'entries')
