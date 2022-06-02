import glob
from timeit import default_timer as timer


class TestService:
    def __init__(self, func, cwd):
        self.func = func
        self.cwd = cwd

    def get_test_data(self):
        files = sorted(glob.glob(self.cwd + "/*.in"), key=lambda x: int(x.split(".")[1]))
        data = []

        for file in files:
            with open(file) as f:
                mf = f.read().rstrip()

                if "\n" in mf:
                    mf = [i for i in mf.split("\n")]
                    mf[0] = float(mf[0])
                    mf[1] = int(mf[1])
                    data.append(mf)
                else:
                    data.append(int(mf))
        return data

    def get_test_results(self):
        files = sorted(glob.glob(self.cwd + "/*.out"), key=lambda x: int(x.split(".")[1]))
        results = []
        for file in files:
            with open(file) as f:
                results.append(f.read())
        return results

    def run_tests(self):
        test_number = 0
        for data, result in zip(self.get_test_data(), self.get_test_results()):
            start = timer()
            my_res = self.func(data)
            end = timer()

            my_res = str(my_res)[:10]
            result = str(result)[:10]
            time = int(end - start)

            if my_res == result:
                print(f"Test#{test_number}, test data - {data}, my result {my_res} == {result} its True\n Elapsed time {time}")
            else:
                print(f"Test#{test_number}, test data - {data}, my result {my_res} != {result} its False\n Elapsed time {time}")
            test_number += 1
