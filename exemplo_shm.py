#!/usr/bin/python3

from multiprocessing import shared_memory, Process
import numpy as np

def child_process_task(shm_name, size):
    """Function executed by a child process to access and modify shared memory."""
    # Attach to the existing shared memory block
    existing_shm = shared_memory.SharedMemory(name=shm_name)

    # Create a NumPy array backed by the shared memory buffer
    shared_array = np.ndarray((size,), dtype=np.int32, buffer=existing_shm.buf)

    print(f"Child process: Original data in shared memory: {shared_array[:]}")

    # Modify the data in shared memory
    shared_array[:] = shared_array[:] * 2
    print(f"Child process: Modified data in shared memory: {shared_array[:]}")

    # Close the shared memory instance in the child process
    existing_shm.close()

if __name__ == "__main__":
    array_size = 5

    # Create a NumPy array in the main process
    original_array = np.arange(array_size, dtype=np.int32)
    print(f"Main process: Original array: {original_array}")

    # Create a shared memory block
    # The size should be sufficient to hold the array's data
    shm = shared_memory.SharedMemory(create=True, size=original_array.nbytes)

    # Create a NumPy array backed by the shared memory buffer
    # and copy the data from the original array
    shared_array_main = np.ndarray((array_size,), dtype=original_array.dtype, buffer=shm.buf)
    shared_array_main[:] = original_array[:]

    print(f"Main process: Data copied to shared memory: {shared_array_main[:]}")

    # Create and start a child process
    p = Process(target=child_process_task, args=(shm.name, array_size))
    p.start()
    p.join()  # Wait for the child process to finish

    print(f"Main process: Data in shared memory after child process: {shared_array_main[:]}")

    # Clean up: close and unlink the shared memory block
    shm.close()
    shm.unlink()
