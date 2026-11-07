# View Serializability Checker


from itertools import permutations


class ViewSerializability:
    def __init__(self):
        self.schedule = [
            ("T1", "WRITE", "A"),
            ("T2", "WRITE", "A"),
            ("T1", "READ", "A"),
            ("T2", "WRITE", "B")
        ]

    def get_view_info(self, schedule):
        last_writer = {}
        reads_from = {}
        final_writes = {}

        for transaction, operation, data in schedule:

            if operation == "READ":
                reads_from[(transaction, data)] = (
                    last_writer.get(data, "INITIAL")
                )

            elif operation == "WRITE":
                last_writer[data] = transaction
                final_writes[data] = transaction

        return reads_from, final_writes

    def check(self):
        transactions = sorted({
            item[0] for item in self.schedule
        })

        original_reads, original_final = self.get_view_info(
            self.schedule
        )

        for order in permutations(transactions):
            serial_schedule = []

            for transaction in order:
                for operation in self.schedule:
                    if operation[0] == transaction:
                        serial_schedule.append(operation)

            serial_reads, serial_final = self.get_view_info(
                serial_schedule
            )

            if (original_reads == serial_reads and
                    original_final == serial_final):

                print("Schedule is View Serializable")
                print("Equivalent Serial Order:", order)
                return

        print("Schedule is NOT View Serializable")


checker = ViewSerializability()
checker.check()
