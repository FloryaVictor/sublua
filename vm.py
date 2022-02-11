import argparse


from compiler.compiler import compile


class VM:
    def __init__(self, bytecode: bytearray) -> None:
        self.bytecode = bytecode
    
    def start(self):
        pass


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='store_true', help='target file is bytecode')
    parser.add_argument("file")
    args = parser.parse_args()
    file = args.file
    
    bytecode = None
    if args.b:
        with open(file, "rb") as f:
            bytecode = bytearray(f.read())
    else:
        bytecode = compile(file)

    print(bytecode)

if __name__ == "__main__":
    main()