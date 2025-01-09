import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to browse and select input video file
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv;*.avi;*.mov")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

# Function to browse and select output folder
def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

# Function to update compression percentage label
def update_compression_label(value):
    compression_label.config(text=f"Compression Percentage: {value}%")

# Function to find ffmpeg in system PATH
def find_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return 'ffmpeg'  # If ffmpeg is found in system PATH
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None  # Not found in system PATH

# Function to compress video
def compress_video():
    input_video = input_entry.get()
    output_dir = output_entry.get()
    compression_percentage = 100 - compression_slider.get()  # Invert the slider value

    # Validate input compression percentage
    if compression_percentage < 1 or compression_percentage > 500:
        messagebox.showerror("Error", "Compression percentage must be between 1 and 500.")
        return

    # Validate input file and output directory
    if not os.path.exists(input_video):
        messagebox.showerror("Error", f"Input video file '{input_video}' does not exist.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare output video path
    output_video = os.path.join(output_dir, os.path.basename(input_video))

    # Find FFmpeg in system PATH
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        # If FFmpeg is not found, prompt user to provide the path
        ffmpeg_path = filedialog.askopenfilename(title="Select FFmpeg executable", filetypes=[("Executable files", "*.exe")])
        if not ffmpeg_path or not os.path.exists(ffmpeg_path):
            messagebox.showerror("Error", "FFmpeg executable not found. Please check your installation.")
            return

    # Calculate the scale factor for video
    scale_factor = 100 / compression_percentage

    # Set default audio bitrate
    audio_bitrate = 12  # Default value if no condition is met

    # Set bitrate for video and audio dynamically
    video_bitrate = int(5019 * compression_percentage / 100)  # Adjust video bitrate based on percentage

    if compression_percentage > 80:
        audio_bitrate = 48  # Very high compression, lowest bitrate
    elif compression_percentage > 50:
        audio_bitrate = 24  # Moderate compression, lower bitrate
    elif compression_percentage > 20:
        audio_bitrate = 12  # Light compression, medium bitrate
    elif compression_percentage > 10:
        audio_bitrate = 8  # Minimal compression, highest bitrate

    # Build the FFmpeg command
    command = [
        ffmpeg_path,
        "-i", input_video,
        "-vf", f"scale=trunc(iw/{scale_factor}/2)*2:trunc(ih/{scale_factor}/2)*2:flags=neighbor",  # Compress video
        "-b:v", f"{video_bitrate}k",  # Video bitrate
        "-crf", "51",  # Constant Rate Factor for video quality
        "-preset", "ultrafast",  # Encoding speed
        "-b:a", f"{audio_bitrate}k",  # Aggressive audio compression
        "-acodec", "aac",  # Audio codec
        "-y", output_video  # Output file path
    ]

    # Run the FFmpeg command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        messagebox.showinfo("Success", f"Video and audio compression successful! Output saved to {output_video}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error compressing video: {e}\n\nstdout:\n{e.stdout.decode()}\nstderr:\n{e.stderr.decode()}")
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"Error: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Video and Audio Compressor")

# Input file selection
input_frame = tk.Frame(root)
input_frame.pack(pady=10, padx=10, fill=tk.X)
input_label = tk.Label(input_frame, text="Input Video:")
input_label.pack(side=tk.LEFT)
input_entry = tk.Entry(input_frame, width=50)
input_entry.pack(side=tk.LEFT, padx=5)
input_button = tk.Button(input_frame, text="Browse", command=select_input_file)
input_button.pack(side=tk.LEFT)

# Output folder selection
output_frame = tk.Frame(root)
output_frame.pack(pady=10, padx=10, fill=tk.X)
output_label = tk.Label(output_frame, text="Output Folder:")
output_label.pack(side=tk.LEFT)
output_entry = tk.Entry(output_frame, width=50)
output_entry.pack(side=tk.LEFT, padx=5)
output_button = tk.Button(output_frame, text="Browse", command=select_output_folder)
output_button.pack(side=tk.LEFT)

# Compression percentage slider
compression_frame = tk.Frame(root)
compression_frame.pack(pady=10, padx=10)
compression_label = tk.Label(compression_frame, text="Compression Percentage: 50%")  # Default label
compression_label.pack()
compression_slider = tk.Scale(compression_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=update_compression_label)
compression_slider.set(50)  # Set default value to 50
compression_slider.pack()

# Compress button
compress_button = tk.Button(root, text="Compress Video", command=compress_video)
compress_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()