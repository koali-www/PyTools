import re
import pathlib
# import pathlib2
import filecmp
from pathlib import Path
from hashlib import md5
import shutil
from collections import defaultdict
from typing import Mapping


def ChangeFileName(basedir, FileRegex):
    '''
        批量修改文件名,传入参数参考：'* - * - *.mp3'
    '''
    files = pathlib.Path(basedir).glob(FileRegex)
    for path in files:
        print(path.name)
        rename = re.sub(r"[0-9]{13} - ", "", path.name)
        try:
            path.rename(pathlib.Path(basedir+"\\"+rename))
        except:
            # 如果更名后的文件存在就删除
            path.unlink()


def Merge(OriginalPath, TargetPath, FileRegex="*",):
    '''
        看起来很麻烦的递归合并文件夹，但不检测文件hash
    '''
    Originalfiles = pathlib.Path(OriginalPath).glob(FileRegex)
    Targetfiles = pathlib.Path(TargetPath)
    # 遍历源目录
    for file in Originalfiles:
        # 目标文件路径
        Targetfile = Targetfiles / file.name
        if file.is_file():
            if Targetfile.exists():
                print("文件存在了：", Targetfile)
            else:
                # 文件不存在就复制到目标文件夹
                print("复制文件到目标文件夹：", file)
                shutil.copy(file, Targetfiles)
        elif file.is_dir():
            if not Targetfile.exists():
                print("文件夹不存在，创建：", Targetfile)
                Targetfile.mkdir()
            Merge(file, Targetfile)


def FolderMerge(OriginalPath, TargetPath):
    '''
    不保熟的文件夹合并
    '''
    OriginalFiles = pathlib.Path(OriginalPath)
    TargetFiles = pathlib.Path(TargetPath)
    result = filecmp.dircmp(OriginalFiles, TargetFiles)

    print(result.left_only)
    # 找到源文件里独有的文件，复制到目标文件
    for file in result.left_only:
        filepath = OriginalFiles / file
        if filepath.is_file():
            print(filepath)
            shutil.copy(filepath, TargetPath)
        elif filepath.is_dir():
            print(filepath, TargetPath)
            shutil.copytree(filepath, TargetPath)

    print(result.report())


def FileHash(path, FileRegex):
    hashmap: Mapping[str, str] = defaultdict()
    # print(hashmap)
    for file in path.glob(FileRegex):
        if file.is_file():
            hash = md5(file.read_bytes()).hexdigest()
            hashmap[hash] = file.name
            # print(hashmap)
    return hashmap


def FolderMergePlus(OriginalPath, TargetPath, FileRegex="*"):
    '''
    比较保熟的文件夹合并，支持指定文件后缀
    '''
    OriginalFiles = pathlib.Path(OriginalPath)
    TargetFiles = pathlib.Path(TargetPath)

    # print(filehash(OriginalFiles))
    # print(filehash(TargetFiles))

    OriginalHash = FileHash(OriginalFiles, FileRegex)
    # 合并到Target,文件相同但文件名不同的用target内的文件名
    TargetHash = FileHash(TargetFiles, FileRegex)
    print(TargetHash)
    print(OriginalHash)

    '''
        文件名相同但文件不同的情况：original内的文件重命名，复制到target
        文件名不相同但文件相同的情况：保留target内的
    '''
    for file in OriginalHash:
        # print(OriginalHash[file])
        if(file in TargetHash):
            pass
        elif (OriginalHash[file] in TargetHash.values()):
            print("重复文件:", OriginalHash[file], "，修改为.copy.xx后缀")
            # print(OriginalFiles/OriginalHash[file])
            shutil.copy(pathlib.Path(OriginalFiles/OriginalHash[file]), pathlib.Path(
                TargetFiles/OriginalHash[file]).with_suffix('.copy'+pathlib.Path(
                    TargetFiles/OriginalHash[file]).suffix))
        else:
            try:
                print("复制文件：", OriginalHash[file])
                shutil.copy2(pathlib.Path(
                    OriginalFiles/OriginalHash[file]), TargetPath)
            except:
                print("文件存在了", TargetHash[file])
