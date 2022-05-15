import glob


class TestService:
    def __init__(self, func, cwd):
        self.func = func
        self.cwd = cwd

    def get_test_data(self):
        files = sorted(glob.glob(self.cwd + "/*.in"), key=lambda x: x.split(".")[1])
        data = []
        for file in files:
            with open(file) as f:
                data.append(int(f.read()))
        return data

    def get_test_results(self):
        files = sorted(glob.glob(self.cwd + "/*.out"), key=lambda x: x.split(".")[1])
        results = []
        for file in files:
            with open(file) as f:
                results.append(int(f.read()))
        return results

    def run_tests(self):
        for data, result in zip(self.get_test_data(), self.get_test_results()):
            if self.func(data) == result:
                print(f"{data} test == {result} its True")
            else:
                print(f"{data} != {result} its False")
