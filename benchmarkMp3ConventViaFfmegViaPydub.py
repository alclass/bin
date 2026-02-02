#!/usr/bin/env python3
"""
~/bin/benchmarkMp3ConventViaFfmegViaPydub.py

python3 benchmark_mp3.py -b 128k -r 44100 -i ./media_folder
python3 benchmark_mp3_chart.py -b 128k -r 44100 -i ./media_folder --chart results.png
python3 benchmark_mp3_chart.py -b 128k -r 44100 -i ./media_folder --csv results.csv --chart results.png

--- Benchmark Results ---
FFmpeg:
  Total time: 12.34 s
  Avg/file:   1.03 s
  CPU time:   8.56 s
  Peak memory: 45.67 MB

Pydub:
  Total time: 18.90 s
  Avg/file:   1.57 s
  CPU time:   12.34 s
  Peak memory: 78.90 MB

Insights
========

  1 FFmpeg tends to be faster and leaner in memory.
  2 Pydub adds Python overhead and may use more memory,
    but is easier to integrate into Python workflows.

"""
import argparse
import os
import subprocess
import sys
import time
import psutil
import csv
import matplotlib.pyplot as plt
from pydub import AudioSegment

# --- Conversion Functions ---


def convert_ffmpeg(input_file, output_dir, bitrate, samplerate):
  filename = os.path.splitext(os.path.basename(input_file))[0] + "_ffmpeg.mp3"
  output_file = os.path.join(output_dir, filename)

  cmd = [
      "ffmpeg",
      "-i", input_file,
      "-vn",  # no video
      "-ar", str(samplerate),
      "-ab", bitrate,
      "-f", "mp3",
      output_file
  ]
  subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def convert_pydub(input_file, output_dir, bitrate, samplerate):
  filename = os.path.splitext(os.path.basename(input_file))[0] + "_pydub.mp3"
  output_file = os.path.join(output_dir, filename)

  audio = AudioSegment.from_file(input_file)
  audio = audio.set_frame_rate(samplerate)
  audio.export(output_file, format="mp3", bitrate=bitrate)


# --- Benchmark Runner ---

def benchmark(files, output_dir, bitrate, samplerate, method):
  process = psutil.Process(os.getpid())
  cpu_times_start = process.cpu_times()
  mem_info_start = process.memory_info().rss

  start = time.time()
  if method == "ffmpeg":
    for f in files:
      convert_ffmpeg(f, output_dir, bitrate, samplerate)
  elif method == "pydub":
    for f in files:
      convert_pydub(f, output_dir, bitrate, samplerate)
  end = time.time()

  cpu_times_end = process.cpu_times()
  mem_info_end = process.memory_info().rss

  elapsed = end - start
  cpu_used = (cpu_times_end.user - cpu_times_start.user) + (cpu_times_end.system - cpu_times_start.system)
  mem_peak = max(mem_info_start, mem_info_end)

  return {
      "method": method,
      "time_total": elapsed,
      "time_avg": elapsed / len(files),
      "cpu_time": cpu_used,
      "mem_peak_MB": mem_peak / (1024 * 1024)
  }


def export_csv(results, csv_file, num_files, bitrate, samplerate):
  header = ["method", "bitrate", "samplerate", "num_files", "time_total", "time_avg", "cpu_time", "mem_peak_MB"]
  write_header = not os.path.exists(csv_file)

  with open(csv_file, mode="a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    if write_header:
      writer.writeheader()
    for res in results:
      row = {
          "method": res["method"],
          "bitrate": bitrate,
          "samplerate": samplerate,
          "num_files": num_files,
          "time_total": f"{res['time_total']:.2f}",
          "time_avg": f"{res['time_avg']:.2f}",
          "cpu_time": f"{res['cpu_time']:.2f}",
          "mem_peak_MB": f"{res['mem_peak_MB']:.2f}"
      }
      writer.writerow(row)


def generate_chart(results, output_file="benchmark_chart.png"):
  methods = [res["method"] for res in results]
  metrics = ["time_total", "time_avg", "cpu_time", "mem_peak_MB"]

  fig, axs = plt.subplots(2, 2, figsize=(10, 8))
  axs = axs.flatten()

  for i, metric in enumerate(metrics):
    values = [res[metric] for res in results]
    axs[i].bar(methods, values, color=["steelblue", "orange"])
    axs[i].set_title(metric.replace("_", " ").capitalize())
    axs[i].set_ylabel("Value")
    axs[i].set_xlabel("Method")

  plt.tight_layout()
  plt.savefig(output_file)
  print(f"Chart saved as {output_file}")


def main():
  parser = argparse.ArgumentParser(description="Benchmark ffmpeg vs pydub MP3 conversion with CPU/memory stats and chart.")
  parser.add_argument("-b", "--bitrate", required=True, help="MP3 bitrate (e.g., 64k, 128k)")
  parser.add_argument("-r", "--samplerate", type=int, required=True, help="Sample rate (e.g., 22050, 44100)")
  parser.add_argument("-i", "--input", required=True, help="Input folder with media files")
  parser.add_argument("-o", "--output", default="benchmark_output", help="Output folder")
  parser.add_argument("--csv", help="Optional CSV file to store results")
  parser.add_argument("--chart", help="Optional chart image file (PNG) to save summary", default="benchmark_chart.png")

  args = parser.parse_args()

  if not os.path.isdir(args.input):
    sys.exit("Error: Input must be a folder containing media files.")

  os.makedirs(args.output, exist_ok=True)

  files = [os.path.join(args.input, f) for f in os.listdir(args.input) if os.path.isfile(os.path.join(args.input, f))]

  print(f"Benchmarking {len(files)} files...")

  results_ffmpeg = benchmark(files, args.output, args.bitrate, args.samplerate, "ffmpeg")
  results_pydub = benchmark(files, args.output, args.bitrate, args.samplerate, "pydub")

  results = [results_ffmpeg, results_pydub]

  print("\n--- Benchmark Results ---")
  for res in results:
    print(f"{res['method'].capitalize()}:")
    print(f"  Total time: {res['time_total']:.2f} s")
    print(f"  Avg/file:   {res['time_avg']:.2f} s")
    print(f"  CPU time:   {res['cpu_time']:.2f} s")
    print(f"  Peak memory:{res['mem_peak_MB']:.2f} MB\n")

  # Export to CSV if requested
  if args.csv:
    export_csv(results, args.csv, len(files), args.bitrate, args.samplerate)
    print(f"Results appended to {args.csv}")

  # Generate chart
  generate_chart(results, args.chart)


if __name__ == "__main__":
  main()