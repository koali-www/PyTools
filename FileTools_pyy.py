from pathlib import Path
from hashlib import md5
import shutil
from collections import defaultdict
from typing import Mapping


def get_hashs(dir_path: Path):
    hashmap: Mapping[str, list[Path]] = defaultdict(list)
    for path in dir_path.glob('**/*'):
        if path.is_file():
            hash = md5(path.read_bytes()).hexdigest()
            hashmap[hash].append(path.relative_to(dir_path))
    return hashmap


def fcp(a: Path, b: Path):
    a_hashmap = get_hashs(a)
    b_hashmap = get_hashs(b)

    print('a: ', a_hashmap)
    print('b: ', b_hashmap)

    for a_hash, a_paths in a_hashmap.items():
        if a_hash in b_hashmap:
            for path in a_paths:
                if path not in b_hashmap[a_hash]:
                    b_hashmap[a_hash].append(path)
            continue
        path = a_paths[0]
        print(f"copy {a/path} to {b/path}")
        (b/path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(a/path, b/path)
        b_hashmap[a_hash] = a_paths

    print('a: ', a_hashmap)
    print('b: ', b_hashmap)

    for b_hash, b_paths in b_hashmap.items():
        for path in b_paths:
            if not path.is_symlink() and path.is_file():
                b_paths.remove(path)
                b_paths.insert(0, path)

        for path in b_paths[1:]:
            print(f"delete {b/path}")
            (b/path).unlink(missing_ok=True)
            print(f"link {b/path} to {b/b_hashmap[b_hash][0]}")
            (b/path).absolute().symlink_to((b/b_hashmap[b_hash][0]).absolute())


fcp(Path('a'), Path('b'))
