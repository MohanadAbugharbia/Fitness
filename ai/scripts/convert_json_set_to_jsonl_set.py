#!python3.10
"""
USAGE:
    python3 convert_json_set_to_jsonl_set.py <src_file> <dst_file>
"""
import json
from argparse import ArgumentParser
from pydantic import BaseModel, ValidationError
from typing import Optional, Dict
import os
import time

parser: ArgumentParser = ArgumentParser(description="A tool to convert a json formatted training set into a jsonl formatted training set.")
parser.add_argument("src", type=str, help="Json formatted training set filename")
parser.add_argument("dst", type=str, help="Jsonl formatted training set filename")
parser.add_argument("--override", "-o", action="store_true", help="Overrides the destination file if it already exists.")
parser.add_argument("--verbose", "-v", action="store_true", help="Enables more output")

args = parser.parse_args()

class Excercise(BaseModel):
    sets: int
    reps: int
    rpi: int
    minutes_rest_time: int

class TrainingDay(BaseModel):
    days_rest_after: int
    excercises: Dict[str, Excercise]

class Completion(BaseModel):
    day1: TrainingDay
    day2: Optional[TrainingDay]
    day3: Optional[TrainingDay]
    day4: Optional[TrainingDay]
    day5: Optional[TrainingDay]
    day6: Optional[TrainingDay]
    day7: Optional[TrainingDay]

def make_jsonl_training_set(data: dict) -> list[str]:
    lines: list[str] = []
    for key, value in data.items():
        if verify_completion(value) != True:
            print(f"The completion of prompt '{key}' has an incorrect format!")
            exit(-1)
        line_dict: dict = {
            "prompt" : f"{key} ->",
            "completion" : f"{str(value)} ###"
        }
        line_str: str = f"{json.dumps(line_dict)}\n"
        lines.append(line_str)
        verbose(line_str)
    return lines

def verify_completion(obj: dict) -> bool:
    try:
        Completion.parse_obj(obj)
    except ValidationError as e:
        print(e)
        return False
    return True

def verbose(msg: str) -> None:
    if args.verbose:
        print(f"VERBOSE -> {msg}")

def load_json_file(file: str) -> dict:
    with open(file, "r") as f:
        data: dict = json.load(f)
        verbose(json.dumps(data))
        return data

def file_exits(filename: str) -> bool:
    if os.path.exists(filename):
        verbose(f"File '{filename}' already exists!")
        return True
    else:
        return False

def move_file(src: str, dst: str) -> None:
    os.rename(src, dst)

def write_jsonl(data: dict, filename: str) -> None:
    if not args.override and file_exits(filename):
        timestamp: str = str(int(time.time()))
        new_name: str = filename + timestamp
        verbose(f"Moving old '{filename}' to '{new_name}'!")
        move_file(filename, new_name)
    with open(filename, "w") as f:
        lines: list[str] = make_jsonl_training_set(data)
        for line in lines:
            f.write(line)    

def main():
    src: str = args.src
    dst: str = args.dst
    src_data: dict = load_json_file(src)
    write_jsonl(src_data, dst)
    exit(0)

if __name__ == "__main__":
    main()