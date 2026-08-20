import argparse


def encrypt(input_path: str, output_path: str) -> None:
    print("encrypting!")


def decrypt(input_path: str, output_path: str) -> None:
    print("decrypting!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt a file."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--encrypt", action="store_true", help="Encrypt the input file"
    )
    group.add_argument(
        "--decrypt", action="store_true", help="Decrypt the input file"
    )

    parser.add_argument("--input", required=True,
                        help="Path to the input file")
    parser.add_argument("--output", required=True,
                        help="Path to the output file")

    args = parser.parse_args()

    if args.encrypt:
        encrypt(args.input, args.output)
    elif args.decrypt:
        decrypt(args.input, args.output)

