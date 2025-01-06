import time
from multiprocessing import Process, Queue
from operation import ImageOperation


class MultiProcessImageProcessing:
    """Lớp xử lý ảnh bằng đa tiến trình."""

    def __init__(self, image_path, output_dir, num_processes=4, kernel_size=3):
        self.image_path = image_path
        self.output_dir = output_dir
        self.num_processes = num_processes
        self.kernel_size = kernel_size

    def _worker(self, process_id, num_operations):
        """Hàm chạy xử lý ảnh trong tiến trình."""
        for i in range(num_operations):
            output_path = f"{self.output_dir}/output_process_{process_id}_op_{i}.png"
            operation = ImageOperation(image_path=self.image_path, kernel_size=self.kernel_size)
            operation.process_image(output_path)

    def process(self, num_operations_per_process=1):
        """Chạy xử lý ảnh bằng nhiều tiến trình."""
        processes = []

        for process_id in range(self.num_processes):
            p = Process(
                target=self._worker,
                args=(process_id, num_operations_per_process),
            )
            p.start()
            processes.append(p)

        for p in processes:
            p.join()


def main(image_path, output_dir, num_processes=4, kernel_size=3, num_operations_per_process=1):
    """Chương trình chính."""
    tstart = time.time()

    processor = MultiProcessImageProcessing(
        image_path=image_path,
        output_dir=output_dir,
        num_processes=num_processes,
        kernel_size=kernel_size,
    )
    processor.process(num_operations_per_process=num_operations_per_process)

    tend = time.time()
    print(
        f"Processing completed using {num_processes} processes. Time taken: {tend - tstart:.2f} seconds."
    )


if __name__ == "__main__":
    # Đường dẫn ảnh đầu vào
    input_image_path = "downloaded_image.jpg"
    output_directory = "output_images"

    # Chạy chương trình chính
    main(
        image_path=input_image_path,
        output_dir=output_directory,
        num_processes=4, 
        kernel_size=3,
        num_operations_per_process=2,
    )