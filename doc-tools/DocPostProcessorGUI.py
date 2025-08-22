#!/usr/bin/env python3
"""
Documentation Post-Processor GUI
A graphical interface for cleaning, structuring, and sorting scraped markdown files.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import asyncio
from pathlib import Path
from datetime import datetime
import json
import queue

from DocPostProcessor import DocumentPostProcessor


class DocPostProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Documentation Post-Processor")
        self.root.geometry("1000x800")
        self.root.minsize(700, 600)
        
        # Variables
        self.processing = False
        self.processor_thread = None
        
        # Thread-safe message queue
        self.message_queue = queue.Queue()
        
        # Configure style
        self.setup_styles()
        self.setup_ui()
        
        # Center window and start checking for messages
        self.center_window()
        self.check_messages()
    
    def setup_styles(self):
        """Configure modern styling for the GUI."""
        try:
            style = ttk.Style()
            style.theme_use('clam')
            
            # Configure button styles
            style.configure("Accent.TButton", 
                          background='#007ACC',
                          foreground='white',
                          font=('TkDefaultFont', 9, 'bold'))
            style.map("Accent.TButton",
                     background=[('active', '#005a9e')])
        except Exception:
            pass
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Input Directory
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Input Directory:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.input_var = tk.StringVar(value="Documentation/Anthropic")
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var, width=50)
        self.input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.input_browse_btn = ttk.Button(input_frame, text="Browse", command=lambda: self.browse_directory('input'))
        self.input_browse_btn.grid(row=0, column=2, sticky=tk.W)
        
        # Output Directory
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_var = tk.StringVar(value="processed_docs")
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        self.output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.output_browse_btn = ttk.Button(output_frame, text="Browse", command=lambda: self.browse_directory('output'))
        self.output_browse_btn.grid(row=0, column=2, sticky=tk.W)
        
        # Processing Options Frame
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Chunk Size
        ttk.Label(options_frame, text="Chunk Size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.chunk_size_var = tk.IntVar(value=1000)
        self.chunk_size_spinbox = ttk.Spinbox(
            options_frame, 
            from_=100, 
            to=5000, 
            increment=100,
            textvariable=self.chunk_size_var,
            width=10
        )
        self.chunk_size_spinbox.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        ttk.Label(options_frame, text="tokens").grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # Chunk Overlap
        ttk.Label(options_frame, text="Chunk Overlap:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.chunk_overlap_var = tk.IntVar(value=200)
        self.chunk_overlap_spinbox = ttk.Spinbox(
            options_frame, 
            from_=0, 
            to=1000, 
            increment=50,
            textvariable=self.chunk_overlap_var,
            width=10
        )
        self.chunk_overlap_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        ttk.Label(options_frame, text="tokens").grid(row=1, column=2, sticky=tk.W, padx=(5, 0))
        
        # Process Subfolders
        self.process_subfolders_var = tk.BooleanVar(value=True)
        self.process_subfolders_check = ttk.Checkbutton(
            options_frame,
            text="Process all subfolders recursively",
            variable=self.process_subfolders_var
        )
        self.process_subfolders_check.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Flatten Output
        self.flatten_output_var = tk.BooleanVar(value=True)
        self.flatten_output_check = ttk.Checkbutton(
            options_frame,
            text="Flatten output (consolidate all files in single folder)",
            variable=self.flatten_output_var
        )
        self.flatten_output_check.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Use LLM Classification
        self.use_llm_var = tk.BooleanVar(value=False)
        self.use_llm_check = ttk.Checkbutton(
            options_frame,
            text="Use LLM for Classification (requires OpenAI API key)",
            variable=self.use_llm_var,
            command=self.toggle_api_key
        )
        self.use_llm_check.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # API Key (hidden by default)
        self.api_key_label = ttk.Label(options_frame, text="API Key:")
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(options_frame, textvariable=self.api_key_var, show="*", width=40)
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.process_btn = ttk.Button(
            button_frame, 
            text="Start Processing", 
            command=self.start_processing,
            style="Accent.TButton"
        )
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            button_frame, 
            text="Stop", 
            command=self.stop_processing,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            button_frame, 
            text="Clear Log", 
            command=self.clear_log
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Statistics Frame
        stats_frame = ttk.LabelFrame(main_frame, text="Processing Statistics", padding="5")
        stats_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=4, wrap=tk.WORD, bg='#f0f0f0')
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        self.stats_text.insert(tk.END, "No processing statistics yet...")
        self.stats_text.config(state=tk.DISABLED)
        
        # Log Output
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=15,
            bg='#f0f0f0'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready to process documents")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN
        )
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def browse_directory(self, dir_type):
        """Open directory browser."""
        directory = filedialog.askdirectory()
        if directory:
            if dir_type == 'input':
                self.input_var.set(directory)
            else:
                self.output_var.set(directory)
    
    def toggle_api_key(self):
        """Show/hide API key field based on checkbox."""
        if self.use_llm_var.get():
            self.api_key_label.grid(row=5, column=0, sticky=tk.W, pady=5)
            self.api_key_entry.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        else:
            self.api_key_label.grid_remove()
            self.api_key_entry.grid_remove()
    
    def check_messages(self):
        """Check for messages from processor thread."""
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                
                if msg_type == "log":
                    self._log_to_widget(data["message"], data["level"])
                elif msg_type == "status":
                    self.status_var.set(data)
                elif msg_type == "stats":
                    self._update_stats_widget(data)
                elif msg_type == "complete":
                    self._processing_complete(data)
                elif msg_type == "error":
                    self._processing_error(data)
                    
        except queue.Empty:
            pass
        finally:
            # Schedule next check
            self.root.after(100, self.check_messages)
    
    def _log_to_widget(self, message, level="INFO"):
        """Add message to log widget (called on main thread)."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
    
    def _update_stats_widget(self, stats):
        """Update statistics display (called on main thread)."""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        if stats:
            self.stats_text.insert(tk.END, f"Total Documents: {stats.get('total_documents', 0)}\n")
            self.stats_text.insert(tk.END, f"Total Chunks: {stats.get('total_chunks', 0)}\n")
            self.stats_text.insert(tk.END, f"Categories: ")
            
            categories = stats.get('categories', {})
            cat_text = ", ".join([f"{cat}: {count}" for cat, count in categories.items()])
            self.stats_text.insert(tk.END, cat_text)
        
        self.stats_text.config(state=tk.DISABLED)
    
    def _processing_complete(self, summary):
        """Handle processing completion (called on main thread)."""
        self.processing = False
        self.progress.stop()
        self.process_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        messagebox.showinfo(
            "Success", 
            f"Processing completed!\n\n"
            f"Documents processed: {summary['total_documents']}\n"
            f"Total chunks created: {summary['total_chunks']}\n"
            f"Output saved to: {self.output_var.get()}"
        )
    
    def _processing_error(self, error_msg):
        """Handle processing error (called on main thread)."""
        self.processing = False
        self.progress.stop()
        self.process_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        messagebox.showerror("Error", f"Processing failed:\n{error_msg}")
    
    def log(self, message, level="INFO"):
        """Thread-safe logging."""
        self.message_queue.put(("log", {"message": message, "level": level}))
    
    def clear_log(self):
        """Clear the log text."""
        self.log_text.delete(1.0, tk.END)
    
    def update_status(self, message):
        """Thread-safe status update."""
        self.message_queue.put(("status", message))
    
    def update_stats(self, stats):
        """Thread-safe statistics update."""
        self.message_queue.put(("stats", stats))
    
    def start_processing(self):
        """Start the processing."""
        if self.processing:
            messagebox.showwarning("Warning", "Processing is already in progress!")
            return
        
        # Validate inputs
        input_dir = self.input_var.get().strip()
        output_dir = self.output_var.get().strip()
        
        if not input_dir:
            messagebox.showerror("Error", "Please select an input directory")
            return
        
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
        
        if not Path(input_dir).exists():
            messagebox.showerror("Error", f"Input directory does not exist: {input_dir}")
            return
        
        # Get API key if using LLM
        api_key = None
        if self.use_llm_var.get():
            api_key = self.api_key_var.get().strip()
            if not api_key:
                messagebox.showerror("Error", "Please enter an OpenAI API key for LLM classification")
                return
        
        # Start processing in separate thread
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start(10)
        
        # Get processing options
        process_subfolders = self.process_subfolders_var.get()
        flatten_output = self.flatten_output_var.get()
        
        self.processor_thread = threading.Thread(
            target=self.run_processor,
            args=(input_dir, output_dir, api_key, process_subfolders, flatten_output)
        )
        self.processor_thread.daemon = True
        self.processor_thread.start()
    
    def stop_processing(self):
        """Stop the processing."""
        if self.processing:
            self.processing = False
            self.log("Stopping processor...", "WARNING")
            self.update_status("Stopping...")
    
    def run_processor(self, input_dir, output_dir, api_key, process_subfolders, flatten_output):
        """Run the processor in a separate thread."""
        try:
            self.log(f"Starting document post-processing", "INFO")
            self.log(f"Input directory: {input_dir}", "INFO")
            self.log(f"Output directory: {output_dir}", "INFO")
            self.log(f"Process subfolders: {'Yes' if process_subfolders else 'No'}", "INFO")
            self.log(f"Flatten output: {'Yes' if flatten_output else 'No'}", "INFO")
            self.log(f"Using LLM: {'Yes' if api_key else 'No'}", "INFO")
            self.update_status("Processing documents...")
            
            # Create new event loop for thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Create processor with custom logger
            processor = GUIProcessor(input_dir, output_dir, api_key, self, 
                                   process_subfolders=process_subfolders, 
                                   flatten_output=flatten_output)
            
            # Set chunk parameters
            processor.structurer.chunk_size = self.chunk_size_var.get()
            processor.structurer.chunk_overlap = self.chunk_overlap_var.get()
            
            # Run processor
            summary = loop.run_until_complete(processor.process_all_documents(
                recursive=process_subfolders, 
                flatten_output=flatten_output
            ))
            
            # Update statistics
            self.update_stats(summary)
            
            self.log("Processing completed successfully!", "SUCCESS")
            self.update_status("Processing completed")
            
            # Send completion message
            self.message_queue.put(("complete", summary))
            
        except Exception as e:
            self.log(f"Error during processing: {str(e)}", "ERROR")
            self.update_status("Error occurred")
            self.message_queue.put(("error", str(e)))
            
        finally:
            loop.close()


class GUIProcessor(DocumentPostProcessor):
    """Custom processor that logs to GUI."""
    
    def __init__(self, input_dir, output_dir, api_key, gui, process_subfolders=True, flatten_output=True):
        super().__init__(input_dir, output_dir, api_key)
        self.gui = gui
        self.process_subfolders = process_subfolders
        self.flatten_output = flatten_output
    
    async def process_document(self, file_path):
        """Override to add GUI logging."""
        if not self.gui.processing:
            return None
        
        self.gui.log(f"Processing: {file_path.name}")
        result = await super().process_document(file_path)
        
        if result:
            self.gui.log(f"✓ Processed: {result.title} ({len(result.chunks)} chunks)")
            self.gui.update_status(f"Processed {len(self.processed_docs)} documents")
        else:
            self.gui.log(f"✗ Skipped: {file_path.name} (no content)", "WARNING")
        
        return result


def main():
    """Main entry point."""
    try:
        root = tk.Tk()
        
        # Set window icon if available
        try:
            root.iconname("Documentation Post-Processor")
        except:
            pass
        
        # Handle window closing
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        app = DocPostProcessorGUI(root)
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting GUI: {e}")
        messagebox.showerror("Error", f"Failed to start application:\n{e}")
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main() 