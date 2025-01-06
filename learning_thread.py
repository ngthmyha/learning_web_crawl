import time
import threading
from operation import ImageOperation


class MultiThreadImageProcessing:
    """Lớp xử lý ảnh bằng đa luồng."""

    def __init__(self, image_path, output_dir, num_threads=4, kernel_size=3):
        self.image_path = image_path
        self.output_dir = output_dir
        self.num_threads = num_threads
        self.kernel_size = kernel_size

    def _worker(self, thread_id, num_operations):
        """Hàm chạy xử lý ảnh trong luồng."""
        for i in range(num_operations):
            output_path = f"{self.output_dir}/output_thread_{thread_id}_op_{i}.png"
            operation = ImageOperation(image_path=self.image_path, kernel_size=self.kernel_size)
            operation.process_image(output_path)

    def process(self, num_operations_per_thread=1):
        """Chạy xử lý ảnh bằng nhiều luồng."""
        threads = []

        for thread_id in range(self.num_threads):
            t = threading.Thread(
                target=self._worker,
                args=(thread_id, num_operations_per_thread),
            )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()


def main(image_path, output_dir, num_threads=4, kernel_size=3, num_operations_per_thread=1):
    """Chương trình chính."""
    tstart = time.time()

    processor = MultiThreadImageProcessing(
        image_path=image_path,
        output_dir=output_dir,
        num_threads=num_threads,
        kernel_size=kernel_size,
    )
    processor.process(num_operations_per_thread=num_operations_per_thread)

    tend = time.time()
    print(
        f"Processing completed using {num_threads} threads. Time taken: {tend - tstart:.2f} seconds."
    )


if __name__ == "__main__":
    # Đường dẫn ảnh đầu vào
    input_image_path = "downloaded_image.jpg"
    output_directory = "output_images"

    # Chạy chương trình chính
    main(
        image_path=input_image_path,
        output_dir=output_directory,
        num_threads=4,  # Số luồng
        kernel_size=3,  # Kích thước kernel
        num_operations_per_thread=2,  # Số lần xử lý mỗi luồng
    )
