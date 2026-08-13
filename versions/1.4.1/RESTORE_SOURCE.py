from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
parts=sorted((root/'source-archive').glob('*.hex.*'))
hexdata=''.join(p.read_text().strip() for p in parts)
data=bytes.fromhex(hexdata)
out=root/'YXLand-1.4.1-source-tree.tar.xz'
out.write_bytes(data)
sha=hashlib.sha256(data).hexdigest()
expected='3e37ce14840369ffc3ecd0b61bb740048e732de41af7aad6c2a408d37fd8b8b5'
assert sha==expected,(sha,expected)
print('OK',out.name,sha)
