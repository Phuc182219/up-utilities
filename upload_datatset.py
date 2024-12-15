# from datasets import Dataset, Features, Image
# from pathlib import Path
# from PIL import Image as PILImage
#
# # Xưe lí dataset cùng một lúc nhanh tốn nhiều ram
#
# # Hàm load dataset cho nhiều cặp folder
# def load_train_dataset(folders):
#     img_data = []
#     gt_data = []
#
#     for image_dir, gt_dir in folders:
#         # Lấy danh sách file ảnh HDR và GT
#         images = sorted(Path(image_dir).glob("*.jpg"))
#         groundtruths = sorted(Path(gt_dir).glob("*.jpg"))
#
#         if len(images) != len(groundtruths):
#             raise ValueError(
#                 f"Số lượng ảnh và nhãn không khớp trong cặp folder: {image_dir} và {gt_dir}"
#             )
#
#         # Xử lý tất cả ảnh cùng lúc
#         for img_path, gt_path in zip(images, groundtruths):
#             # Mở ảnh HDR và GT
#             with PILImage.open(img_path) as img:
#                 img_data.append(img.copy())
#
#             with PILImage.open(gt_path) as gt:
#                 gt_data.append(gt.copy())
#
#     # Trả về dataset
#     return Dataset.from_dict({"img": img_data, "gt": gt_data}, features=Features({
#         "img": Image(),  # Cột ảnh HDR
#         "gt": Image(),   # Cột ảnh Ground Truth
#     }))
#
# # Hàm tạo dataset từ các cặp thư mục
# def create_dataset():
#     folders = [
#         (r"D:\good data\10 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\10 Carnation Road - Youngsville, NC_ground_truth"),
#         (r"D:\good data\20 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\20 Carnation Road - Youngsville, NC_ground_truth"),
#         (r"D:\good data\40 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\40 Carnation Road - Youngsville, NC_ground_truth"),
#         (r"D:\good data\108 Blue Haven Dr_hdr_results", r"D:\good data\108 Blue Haven Dr_ground_truth"),
#         (r"D:\good data\410 Nelson Dr_hdr_results", r"D:\good data\410 Nelson Dr_ground_truth"),
#         (r"D:\good data\717 Bayboro Ct_hdr_results", r"D:\good data\717 Bayboro Ct_ground_truth"),
#     ]
#     return load_train_dataset(folders)
#
# # Tạo dataset
# train_dataset = create_dataset()
#
# # Đẩy dataset lên Hugging Face
# train_dataset.push_to_hub("HoangPhuc7678/Good_OJT_dta_aligned")


# # Tạo dataset up lên theo kiểu xử lí từng batch nhỏ tiết kiệm ram
# train_dataset = create_dataset()

# # Đẩy dataset lên Hugging Face Hub
# train_dataset.push_to_hub("HoangPhuc7678/Good_OJT_dta_aligned")


# from datasets import Dataset, Features, Image, Value
# from pathlib import Path
# from PIL import Image as PILImage
# import os
#
# # Hàm load dataset cho nhiều cặp folder (đã sửa đổi)
# def load_train_dataset(folders, batch_size=10):
#     def generate_data():
#         for image_dir, gt_dir in folders:
#             # Lấy danh sách file ảnh và ground truth trong mỗi folder
#             images = sorted(Path(image_dir).glob("*.jpg"))
#             groundtruths = sorted(Path(gt_dir).glob("*.jpg"))
#
#             if len(images) != len(groundtruths):
#                 raise ValueError(
#                     f"Số lượng ảnh và nhãn không khớp trong cặp folder: {image_dir} và {gt_dir}"
#                 )
#
#             # Xử lý theo từng đợt nhỏ hơn
#             for i in range(0, len(images), batch_size):
#                 batch_images = images[i : i + batch_size]
#                 batch_groundtruths = groundtruths[i : i + batch_size]
#
#                 for img_path, gt_path in zip(batch_images, batch_groundtruths):
#                     # Mở ảnh HDR
#                     with PILImage.open(img_path) as img:
#                         hdr_img = img.copy()
#
#                     # Mở ảnh GT
#                     with PILImage.open(gt_path) as gt:
#                         gt_img = gt.copy()
#
#                     # Trả dữ liệu về generator
#                     yield {
#                         "img": hdr_img,  # Ảnh HDR
#                         "gt": gt_img,    # Ảnh Ground Truth
#                     }
#
#     # Định nghĩa features cho dataset
#     features = Features({
#         "img": Image(),  # Cột ảnh HDR
#         "gt": Image(),   # Cột ảnh Ground Truth
#     })
#
#     # Tạo dataset từ generator function
#     dataset = Dataset.from_generator(generate_data, features=features)
#
#     return dataset
#
# # Hàm tạo dataset với các cặp folder đúng vị trí
# def create_dataset():
#     # Danh sách các cặp folder
#     folders = [
#         (r"D:\good data\10 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\10 Carnation Road - Youngsville, NC_ground_truth"),
#         (r"D:\good data\20 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\20 Carnation Road - Youngsville, NC_ground_truth"),
#         (r"D:\good data\40 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\40 Carnation Road - Youngsville, NC_ground_truth"),
#         (r"D:\good data\108 Blue Haven Dr_hdr_results", r"D:\good data\108 Blue Haven Dr_ground_truth"),
#         (r"D:\good data\410 Nelson Dr_hdr_results", r"D:\good data\410 Nelson Dr_ground_truth"),
#         (r"D:\good data\717 Bayboro Ct_hdr_results", r"D:\good data\717 Bayboro Ct_ground_truth"),
#         # Thêm các cặp folder khác nếu cần
#     ]
#     # Load dataset từ tất cả các folder
#     train_dataset = load_train_dataset(folders)
#     return train_dataset
#
# # Tạo dataset
# train_dataset = create_dataset()
#
# # Đẩy dataset HDR-only lên Hugging Face Hub
# train_dataset.push_to_hub("HoangPhuc7678/Good_OJT_dta_aligned")
#
# # Đẩy toàn bộ dataset (bao gồm cả HDR và GT) nếu cần
# # train_dataset.push_to_hub("HoangPhuc7678/Good_OJT_dta_aligned_with_gt")

# from datasets import Dataset, Features, Image
# from pathlib import Path
# from PIL import Image as PILImage
#
# # Hàm tạo dataset từ ảnh bổ sung
# def load_additional_dataset(folder_path):
#     img_data = []
#     gt_data = []
#
#     # Tìm các file HDR và GT
#     hdr_images = sorted(Path(folder_path).glob("*.png"))
#     gt_images = sorted(Path(folder_path).glob("*.jpg"))
#
#     if len(hdr_images) != len(gt_images):
#         raise ValueError(f"Số lượng ảnh HDR và GT không khớp trong thư mục: {folder_path}")
#
#     for hdr_file, gt_file in zip(hdr_images, gt_images):
#         with PILImage.open(hdr_file) as img:
#             img_data.append(img.copy())
#         with PILImage.open(gt_file) as gt:
#             gt_data.append(gt.copy())
#
#     return Dataset.from_dict({"img": img_data, "gt": gt_data}, features=Features({
#         "img": Image(),
#         "gt": Image(),
#     }))
#
# additional_folder = r"D:\good data\Exterior\20 Carnation Road - Youngsville, NC"
#
# train_dataset = load_additional_dataset(additional_folder)
#
# train_dataset.push_to_hub("HoangPhuc7678/Good_OJT_dta_exterior_aligned")


from datasets import Dataset, Features, Image
from pathlib import Path
from PIL import Image as PILImage

# Hàm load dataset từ các thư mục nội thất
def load_interior_dataset(folders):
    img_data = []
    gt_data = []

    for image_dir, gt_dir in folders:
        images = sorted(Path(image_dir).glob("*.jpg"))
        groundtruths = sorted(Path(gt_dir).glob("*.jpg"))

        if len(images) != len(groundtruths):
            raise ValueError(f"Số lượng ảnh HDR và GT không khớp trong thư mục: {image_dir} và {gt_dir}")

        for img_path, gt_path in zip(images, groundtruths):
            with PILImage.open(img_path) as img:
                img_data.append(img.copy())
            with PILImage.open(gt_path) as gt:
                gt_data.append(gt.copy())

    return img_data, gt_data

# Hàm load dataset từ các thư mục ngoại thất
def load_exterior_dataset(folders):
    img_data = []
    gt_data = []

    for folder in folders:
        hdr_images = sorted(Path(folder).glob("*.png"))
        gt_images = sorted(Path(folder).glob("*.jpg"))

        if len(hdr_images) != len(gt_images):
            raise ValueError(f"Số lượng ảnh HDR và GT không khớp trong thư mục: {folder}")

        for hdr_file, gt_file in zip(hdr_images, gt_images):
            with PILImage.open(hdr_file) as hdr:
                img_data.append(hdr.copy())
            with PILImage.open(gt_file) as gt:
                gt_data.append(gt.copy())

    return img_data, gt_data

# Hàm tạo dataset hợp nhất (nội thất + ngoại thất)
def create_combined_dataset():
    # Danh sách các thư mục nội thất
    interior_folders = [
        (r"D:\good data\10 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\10 Carnation Road - Youngsville, NC_ground_truth"),
        (r"D:\good data\20 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\20 Carnation Road - Youngsville, NC_ground_truth"),
        (r"D:\good data\40 Carnation Road - Youngsville, NC_hdr_results", r"D:\good data\40 Carnation Road - Youngsville, NC_ground_truth"),
        (r"D:\good data\108 Blue Haven Dr_hdr_results", r"D:\good data\108 Blue Haven Dr_ground_truth"),
        (r"D:\good data\410 Nelson Dr_hdr_results", r"D:\good data\410 Nelson Dr_ground_truth"),
        (r"D:\good data\717 Bayboro Ct_hdr_results", r"D:\good data\717 Bayboro Ct_ground_truth"),
        # Thêm các thư mục khác nếu cần
    ]

    # Danh sách các thư mục ngoại thất
    exterior_folders = [
        r"D:\good data\Exterior\20 Carnation Road - Youngsville, NC",
        r"D:\good data\Exterior\40 Carnation Road - Youngsville, NC",
        # Thêm các thư mục khác nếu cần
    ]

    # Load dữ liệu nội thất
    interior_img, interior_gt = load_interior_dataset(interior_folders)

    # Load dữ liệu ngoại thất
    exterior_img, exterior_gt = load_exterior_dataset(exterior_folders)

    # Kết hợp dữ liệu
    combined_img = interior_img + exterior_img
    combined_gt = interior_gt + exterior_gt

    # Tạo dataset
    features = Features({
        "img": Image(),
        "gt": Image(),
    })
    combined_dataset = Dataset.from_dict({
        "img": combined_img,
        "gt": combined_gt,
    }, features=features)

    return combined_dataset

# Tạo dataset hợp nhất
dataset = create_combined_dataset()

# Đẩy dataset lên Hugging Face
dataset.push_to_hub("HoangPhuc7678/Good_OJT_full_aligned_data")

