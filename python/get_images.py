import shutil
from pathlib import Path


image_source_folder = Path(r"C:\Users\wslid\Pictures\photo_data_images")
image_destination_folder = Path("images/original").resolve()  # absolute, based on cwd


def get_local_images():
    print(f"CWD:          {Path.cwd()}")
    print(f"Source:       {image_source_folder}  exists={image_source_folder.exists()}")
    print(f"Destination:  {image_destination_folder}")

    image_destination_folder.mkdir(parents=True, exist_ok=True)

    patterns = ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG")
    files = []
    for pattern in patterns:
        files.extend(image_source_folder.rglob(pattern))

    files = [p for p in files if p.is_file()]
    print(f"Found {len(files)} image(s)")

    for img_file_path in files:
        dest_path = image_destination_folder / img_file_path.name

        # avoid silent overwrite
        if dest_path.exists():
            stem = img_file_path.stem
            suffix = img_file_path.suffix.lower()
            i = 1
            while dest_path.exists():
                dest_path = image_destination_folder / f"{stem}_{i}{suffix}"
                i += 1

        try:
            shutil.move(str(img_file_path), str(dest_path))
            print(f"Moved: {img_file_path} → {dest_path}")
        except Exception as e:
            print(f"Failed: {img_file_path} → {e}")