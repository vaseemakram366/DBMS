# Database Write Amplification Analyzer


class WriteAmplificationAnalyzer:
    def __init__(self):
        self.logical_bytes = 0
        self.physical_bytes = 0
        self.flush_bytes = 0
        self.compaction_bytes = 0
        self.compaction_read_bytes = 0

    def record_logical_write(self, size):
        if size < 0:
            raise ValueError("Write size cannot be negative")
        self.logical_bytes += size

    def record_flush(self, size):
        if size < 0:
            raise ValueError("Flush size cannot be negative")

        self.flush_bytes += size
        self.physical_bytes += size

    def record_compaction(self, read_bytes, written_bytes):
        if read_bytes < 0 or written_bytes < 0:
            raise ValueError("Byte counts cannot be negative")

        self.compaction_read_bytes += read_bytes
        self.compaction_bytes += written_bytes
        self.physical_bytes += written_bytes

    def report(self):
        print("===== Write Amplification Report =====")
        print(f"Logical bytes written:   {self.logical_bytes}")
        print(f"Flush bytes written:     {self.flush_bytes}")
        print(f"Compaction bytes written:{self.compaction_bytes}")
        print(f"Physical bytes written:  {self.physical_bytes}")
        print(f"Compaction bytes read:   {self.compaction_read_bytes}")

        if self.logical_bytes == 0:
            print("Write amplification: N/A (no logical writes)")
        else:
            ratio = self.physical_bytes / self.logical_bytes
            print(f"Write amplification:     {ratio:.2f}x")


analyzer = WriteAmplificationAnalyzer()

# First batch of application writes
analyzer.record_logical_write(1000)
analyzer.record_flush(1000)
analyzer.record_compaction(
    read_bytes=1000,
    written_bytes=700
)

# Second batch of application writes
analyzer.record_logical_write(500)
analyzer.record_flush(500)
analyzer.record_compaction(
    read_bytes=1200,
    written_bytes=400
)

analyzer.report()
