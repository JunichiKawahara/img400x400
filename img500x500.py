import os
import subprocess
from PIL import Image


def expand2square(filename, outputFilename):
    """ 短辺に余白を追加して、正方形の画像にリサイズする

    Parameters
    ----------
    filename: str
        処理対象の画像ファイル名
    outputFilename: str
        出力ファイル名
    """
    result_size = (500, 500)

    if not os.path.isfile(filename):
        return

    im = Image.open(filename)
    bk = (255, 255, 255) if im.mode == 'RGB' else (0, 0, 0, 0)

    # 短辺に余白を追加する
    width, height = im.size
    l = width if width > height else height

    canvas = Image.new(im.mode, (l, l), bk)

    if width > height:
        canvas.paste(im, (0, (width - height) // 2))
    else:
        canvas.paste(im, ((height - width) // 2, 0))

    # リサイズ
    resized = canvas.resize(result_size, Image.LANCZOS)

    resized.save(outputFilename, quality=100)


def aiToJpeg(filename, outputFilename):
    """.ai形式のファイルをjpeg形式に変換する

    Parameters
    ----------
    filename: str
        処理対象の画像ファイル名
    outputFilename: str
        出力ファイル名
    """
    if not os.path.isfile(filename):
        return

    command = [
        "/Users/kawahara/projects/sandbox/img500x500/aiToJpg.sh",
        filename,
        outputFilename
    ]

    subprocess.run(command)


def convert(filename, outputFilename):
    """ファイル形式の変換
    Parameters
    ----------
    filenae: str
        処理対象のファイル名
    """
    root, ext = os.path.splitext(filename)

    log = filename

    if ext == '.ai' or ext == '.psd':
        # ai ファイル
        # ImageMagick コマンドでJPEG形式に変換する
        temp_filename = outputFilename + '_temp.jpg'
        aiToJpeg(filename, temp_filename)
        expand2square(temp_filename, outputFilename)
        if os.path.isfile(temp_filename):
            os.unlink(temp_filename)
    elif ext == '.eps' or ext == '.jpg' or ext == '.bmp' or ext == '.png':
        expand2square(filename, outputFilename)
    else:
        log += "  ignore"

    print(log)


def proc(level, inputFolder, outputFolder):
    """メイン処理

    Pamareters
    ----------
    level: int
        フォルダの階層レベル
    inputFolder: str
        処理対象のフォルダ
    ouputFolder: str
        出力対象のフォルダ
    """

    indent = '  ' * level
    for foldername, subfolders, filenames in os.walk(inputFolder):
        # 出力先フォルダが存在しない場合、フォルダを作成する
        outPath = os.path.join(outputFolder, foldername)
        if not os.path.isdir(outPath):
            os.makedirs(outPath)

        for filename in filenames:
            # ファイルの処理
            inputFilename = os.path.join(foldername, filename)

            fname, ext = os.path.splitext(os.path.basename(filename))
            outputFilename = os.path.join(outPath, (fname + '.jpg'))

            convert(inputFilename, outputFilename)

        for subfolder in subfolders:
            # サブフォルダの処理（当関数を再帰的に呼び出す）
            proc(level + 1, subfolder, outputFolder)

if __name__ == '__main__':
    proc(0, 'datas', 'out')
