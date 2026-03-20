from argparse import ArgumentParser
import csv
import os


def main():

    parser = ArgumentParser()

    parser.add_argument("-i", "--input", help="csv file to be converted.")
    parser.add_argument("-o", "--output", help="txt files destination.")

    args = parser.parse_args()

    if args.input and args.output:
        file_path = str(args.input)

        with open(file_path, "r") as csv_file:
            records: list[str] = []

            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                records.append(row[0])

            for i, record in enumerate(records):
                if not os.path.exists(args.output):
                    os.makedirs(args.output)

                with open(f"{args.output}/{i + 1}.txt", "w") as out_file:
                    out_file.write(record)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
