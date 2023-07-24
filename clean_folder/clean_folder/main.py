from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize

def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)  # TODO: Check!
    except shutil.ReadError:
        print('It is not an archive')
        folder_for_file.rmdir()
    filename.unlink()

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main(folder: Path):
    parser.scan(folder)
    
    # Images
    for file in parser.JPEG_IMAGES + parser.JPG_IMAGES + parser.PNG_IMAGES + parser.SVG_IMAGES:
        handle_media(file, folder / 'images')

    # Videos
    for file in parser.AVI_VIDEOS + parser.MP4_VIDEOS + parser.MOV_VIDEOS + parser.MKV_VIDEOS:
        handle_media(file, folder / 'videos')

    # Documents
    for file in parser.DOC_DOCUMENTS + parser.DOCX_DOCUMENTS + parser.TXT_DOCUMENTS + parser.PDF_DOCUMENTS + parser.XLSX_DOCUMENTS + parser.PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents')

    # Audio
    for file in parser.MP3_AUDIO + parser.OGG_AUDIO + parser.WAV_AUDIO + parser.AMR_AUDIO:
        handle_media(file, folder / 'audio')

    # Archives
    for file in parser.ZIP_ARCHIVES + parser.GZ_ARCHIVES + parser.TAR_ARCHIVES:
        handle_archive(file, folder / 'archives')

    for file in parser.MY_OTHER:
        handle_other(file, folder / 'unknown')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

def start():
    if len(sys.argv) > 1:
        folder_for_scan = Path(sys.argv[1])
        print(f'Starting in folder: {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
    else:
        print("Please provide a folder path as an argument.")


if __name__ == "__main__":
    start()


