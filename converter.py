import os
from subprocess import call, CalledProcessError


class Converter:
    """Класс для конвертации документов с использованием unoconv."""

    @staticmethod
    def convert_to_pdf(output_dir: str, input_file: str):
        if not os.path.exists(input_file):
            raise RuntimeError(f"Input file at path {input_file} does not exist.")

        output_file_path = output_dir

        print(f"Starting conversion: {input_file} to PDF in {output_file_path}")
        try:
            result = call(
                f"unoconv -f pdf -o {output_file_path} {input_file}", shell=True
            )
            print(
                call(f"unoconv -f pdf -o {output_file_path} {input_file}", shell=True)
            )
            if result != 0:
                raise RuntimeError(f"unoconv conversion failed with exit code {result}")
            else:
                print(result)

            if not os.path.exists(output_file_path):
                raise RuntimeError(
                    f"Output file at path {output_file_path} does not exist."
                )

            print(f"Conversion completed. Output file located in: {output_file_path}")
        except CalledProcessError as e:
            raise RuntimeError(f"Error during conversion: {str(e)}")
