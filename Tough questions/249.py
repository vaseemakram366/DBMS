# Database Page Checksum Validation


import hashlib


class PageChecksum:
    def calculate_checksum(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def validate_page(self, data, saved_checksum):
        current_checksum = self.calculate_checksum(data)

        if current_checksum == saved_checksum:
            print("Page validation successful")
            return True

        print("Page corruption detected")
        return False


checker = PageChecksum()

page_data = "Student ID: 101"
saved_checksum = checker.calculate_checksum(page_data)

checker.validate_page(page_data, saved_checksum)

corrupted_data = "Student ID: 999"
checker.validate_page(corrupted_data, saved_checksum)
