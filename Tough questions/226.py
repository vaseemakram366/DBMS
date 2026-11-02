# Wait-Die and Wound-Wait Protocols/


def wait_die(requester_ts, holder_ts):
    if requester_ts < holder_ts:
        return "WAIT"
    return "ABORT"


def wound_wait(requester_ts, holder_ts):
    if requester_ts < holder_ts:
        return "WOUND: abort younger holder"
    return "WAIT"


older = 10
younger = 20

print("Wait-Die:")
print("Older requests younger:", wait_die(older, younger))
print("Younger requests older:", wait_die(younger, older))

print("\nWound-Wait:")
print("Older requests younger:", wound_wait(older, younger))
print("Younger requests older:", wound_wait(younger, older))
