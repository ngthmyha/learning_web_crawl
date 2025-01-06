# image_operation.py
import random
from PIL import Image

class ImageOperation:
    """Lớp xử lý ảnh bằng phép tích chập (convolution)."""

    def __init__(self, image_path, kernel_size=3):
        self.image_path = image_path
        self.kernel_size = kernel_size
        self.kernel = self._init_kernel(kernel_size)

    def _init_kernel(self, size):
        """Khởi tạo kernel ngẫu nhiên."""
        return [[random.uniform(-1.0, 1.0) for _ in range(size)] for _ in range(size)]

    def _convolve_region(self, region):
        """Thực hiện tích chập trên một vùng."""
        kernel_size = self.kernel_size
        result = 0
        for ky in range(kernel_size):
            for kx in range(kernel_size):
                pixel_val = region[ky][kx]
                kernel_val = self.kernel[ky][kx]
                result += pixel_val * kernel_val
        return int(result)

    def process_image(self, output_path):
        """Xử lý ảnh bằng tích chập."""
        with Image.open(self.image_path) as img:
            img = img.convert("L")  # Chuyển sang ảnh grayscale
            pixels = img.load()
            width, height = img.size

            # Kích thước ảnh đầu ra
            result_width = width - self.kernel_size + 1
            result_height = height - self.kernel_size + 1

            # Ảnh kết quả
            result_image = Image.new("L", (result_width, result_height))
            result_pixels = result_image.load()

            # Duyệt qua từng pixel và áp dụng tích chập
            for y in range(result_height):
                for x in range(result_width):
                    # Trích xuất vùng ma trận
                    region = [
                        [pixels[x + kx, y + ky] for kx in range(self.kernel_size)]
                        for ky in range(self.kernel_size)
                    ]
                    # Áp dụng tích chập
                    result_pixels[x, y] = self._convolve_region(region)

            # Lưu ảnh kết quả
            result_image.save(output_path)
