import pathlib


class LoC(object):
    suffixes = ['.py']
    skip = ['name of dir or file to skip', ...]

    def count(self, path, init=True):
        path = pathlib.Path(path)
        if path.name in self.skip:
            print(f'skipped: {path.relative_to(self.root)}')
            return
        if init:
            self.root = path
            self.files = 0
            self.lines = 0
        if path.is_dir():
            # recursive case
            for item in path.iterdir():
                self.count(path=item, init=False)
        elif path.is_file() and path.suffix in self.suffixes:
            # base case
            with path.open(mode='r') as f:
                line_count = len(f.readlines())
            print(f'{path.relative_to(self.root)}: {line_count}')
            self.files += 1
            self.lines += line_count
        if init:
            print(f'\n{self.lines} lines in {self.files} files')

if __name__ == '__main__':
    loc = LoC()
    loc.count('.')
