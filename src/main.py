import argparse
from utils.decrypt import ChessDecrypter
from utils.encrypt import ChessEncrypter


def encrypt(input_path: str, output_path: str) -> None:
    print(f"Encrypting {input_path} to {output_path}")
    encrypter = ChessEncrypter(input_file=input_path, output_dir=output_path)
    encrypter.encrypt()


def decrypt(input_path: str, output_path: str) -> None:
    print(f"Decrypting {input_path} to {output_path}")
    decrypter = ChessDecrypter(input_dir=input_path, output_file=output_path)
    decrypter.decrypt()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encrypt", action="store_true", help="Encrypt the input file")
    group.add_argument("--decrypt", action="store_true", help="Decrypt the input file")

    parser.add_argument("--input", required=True, help="Path to the input file")
    parser.add_argument("--output", required=True, help="Path to the output file")

    args = parser.parse_args()

    if args.encrypt:
        encrypt(args.input, args.output)
    elif args.decrypt:
        decrypt(args.input, args.output)
