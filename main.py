from Project.Services.Calculation import RatioService
from Project.Services.Example_Generation.RandomBilliardSystemService import get_random_billiard_system
from Project.Services.Output.FileWriterService import FileWriterService
import sys

if __name__ == '__main__':
    times = 1000
    max_num = 0
    filewriter = FileWriterService()
    for i in range(times):
        sys.stdout.write(f"\rTry #:{i} ---- Current_Max: {max_num}")
        sys.stdout.flush()
        bs = get_random_billiard_system(t_sides=5, k_sides=5, dim=2)
        RatioService.set_billiard_system_ratio(bs)
        filewriter.write_billiard_system_to_file(bs)
        if bs.ratio > max_num:
            max_num = bs.ratio